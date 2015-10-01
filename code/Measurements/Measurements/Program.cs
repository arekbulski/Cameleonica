using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Runtime.InteropServices;
using System.Threading.Tasks;
using Mono.Unix.Native;

namespace Measurements
{
	class MainClass
	{
		static long ToBytes (string size)
		{
			Dictionary<string,long> suffixes = new Dictionary<string, long> {
				{"KB",1024},
				{"MB",1024*1024},
				{"GB",1024*1024*1024},
				{"TB",1024L*1024*1024*1024},
			};

			foreach (var item in suffixes) {
				if (size.EndsWith(item.Key)) {
					return long.Parse (size.Substring (0, size.Length-item.Key.Length)) * item.Value;
				}
			}
			return long.Parse (size);
		}

		public static void Main (string[] args)
		{
			int AMOUNT = 8000;
			int BLOCK = 512;
			long AREA = 0;

			AREA = ToBytes (args [0]);
			Console.WriteLine ("Amount: " + AMOUNT + "  Block size: " + BLOCK + "  Area: " + AREA);

			string diskpath = args [1];
			int fd = Syscall.open (diskpath, OpenFlags.O_RDONLY);
			if (fd < 0)
				Environment.FailFast ("Could not open the disk.");

			var locations = new long[AMOUNT];
			var times = new double[AMOUNT];
			IntPtr buf = Marshal.AllocHGlobal (BLOCK);

			Random gen = new Random ();
			for (int i = 0; i < locations.Length; i++) {
				locations [i] = (long)(gen.NextDouble () * AREA);
			}

			foreach (var i in Enumerable.Range(0,AMOUNT)) {
				Stopwatch watch = Stopwatch.StartNew ();
				Syscall.pread (fd, buf, (ulong)BLOCK, locations [i]);
				times [i] = watch.Elapsed.TotalMilliseconds;
			}

//			Parallel.For (0, AMOUNT, i => {
//				Stopwatch watch = Stopwatch.StartNew ();
//				Syscall.pread (fd, buf, (ulong)BLOCK, locations[i]);
//				times [i] = watch.Elapsed.TotalMilliseconds;
//			});

			var sum = times.Sum ();
			var timesascending = times.OrderBy (x => x).ToArray ();
			var min95 = timesascending [(int)(0.05 * AMOUNT)];
			var max95 = timesascending [(int)(0.95 * AMOUNT)];

			Console.WriteLine ("Subset of data: " + string.Join (" ", times.Take (4)) + "...");
			Console.WriteLine ("Total: " + sum + "   Average: " + sum / AMOUNT);
			Console.WriteLine ("Min: " + times.Min () + "  of upper 95 percent: " + min95);
			Console.WriteLine ("Max: " + times.Max () + "  of lower 95 percent: " + max95);
		}
	}
}
