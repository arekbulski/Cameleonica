using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Runtime.InteropServices;
using System.Threading.Tasks;
using Mono.Unix.Native;
using System.IO;

namespace Measurements
{
	class MainClass
	{
		static long SuffixToBytes (string size)
		{
			Dictionary<string,long> suffixes = new Dictionary<string, long> {
				{"KB",1024L},
				{"MB",1024L*1024},
				{"GB",1024L*1024*1024},
				{"TB",1024L*1024*1024*1024},
			};

			foreach (var item in suffixes)
				if (size.EndsWith(item.Key))
					return long.Parse (size.Substring (0, size.Length-item.Key.Length)) * item.Value;

			return long.Parse (size);
		}

		static string BytesToSuffix(long size)
		{
			string[] suffixes = {"B","KB","MB","GB","TB","PB","EB","ZB","YB"};

			int suffix = 0;
			while (size % 1024 == 0) {
				suffix++;
				size /= 1024;
			}
			return size.ToString() + suffixes[suffix];
		}

		public static void Main (string[] args)
		{
			long AREA = SuffixToBytes (args [0]);
			long MAXAREA = 1024L*1024*1024*1024; //new FileInfo (args [1]).Length;
			int AMOUNT = 5000;
			int BLOCK = 512;

			Console.WriteLine ("Amount: {0}  Block: {1}  Max area: {2}  Area: {3}",
			                   AMOUNT, BLOCK, BytesToSuffix(MAXAREA), BytesToSuffix(AREA));

			int fd = Syscall.open (args [1], OpenFlags.O_RDONLY);
			if (fd < 0) Environment.FailFast ("Could not open the specified file.");

			var locations1 = new long[AMOUNT];
			var locations2 = new long[AMOUNT];
			var times = new double[AMOUNT];
			IntPtr buf = Marshal.AllocHGlobal (BLOCK);

			Random gen = new Random ();
			foreach (var i in Enumerable.Range(0,AMOUNT)) {
				locations1 [i] = (long)(gen.NextDouble () * (MAXAREA - AREA));
				locations2 [i] = locations1 [i] + (long)(gen.NextDouble () * AREA);
			}

			foreach (var i in Enumerable.Range(0,AMOUNT)) {
				Syscall.pread (fd, buf, (ulong)BLOCK, locations1 [i]);
				Stopwatch watch = Stopwatch.StartNew ();
				Syscall.pread (fd, buf, (ulong)BLOCK, locations2 [i]);
				times [i] = watch.Elapsed.TotalMilliseconds;
			}

			int lower = (int)(0.95 * AMOUNT);
			var timesascending = times.OrderBy(x => x).Take(lower).ToArray();

			Console.WriteLine ("Total: {0:F2}ms  Max: {1:F2}ms  Average: {2:F2}ms", 
			                   times.Sum(), timesascending.Max(), timesascending.Average());
		}
	}
}
