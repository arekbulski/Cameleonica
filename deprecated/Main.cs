using System;
using System.IO;

namespace Cameleonica
{
	class MainClass
	{
		public static void Main (string[] args)
		{
			Console.WriteLine ("Experimental cryptographic filesystem: Cameleonica");
			Console.WriteLine ();

			Console.WriteLine ("Transfer speed from /dev/urandom");
			long M1 = 1024*1024;
			byte[] b = new byte[M1];
			FileStream r = new FileStream("/dev/urandom", FileMode.Open);
			TimeSpan urandtime = Diagnostics.TimeIt( () => { r.Read(b, 0, b.Length); });
			r.Close();
			Console.WriteLine ("Total {0}", urandtime);
			Console.WriteLine ("Speed {0} MB/s", Math.Round(1d / urandtime.TotalSeconds, 2));
			Console.WriteLine ();

			Console.WriteLine ("Creating a container in /tmp/cam1");
			CryptoContainer.CreateContainer("/tmp/cam1", 5000);

			Console.WriteLine ("Opening the container");
			CryptoContainer f = new CryptoContainer("/tmp/cam1");

			Console.WriteLine ("Content of / folder:");
			Console.WriteLine (string.Join(" ",f.ListDirectoryEntries("/")));

			Console.WriteLine ("Creating folder /a");
			f.CreateDirectory("/a");
			Console.WriteLine ("Creating folder /a/b/");
			f.CreateDirectory("/a/b/");
			Console.WriteLine ("Creating folder /a/b/c/");
			f.CreateDirectory("/a/b/c/");

			Console.WriteLine ("Content of / folder:");
			Console.WriteLine (string.Join(" ",f.ListDirectoryEntries("/")));
			Console.WriteLine ("Content of /a/ folder:");
			Console.WriteLine (string.Join(" ",f.ListDirectoryEntries("/a/")));
			Console.WriteLine ("Content of /a/b/ folder:");
			Console.WriteLine (string.Join(" ",f.ListDirectoryEntries("/a/b/")));
			Console.WriteLine ("Content of /a/b/c/ folder:");
			Console.WriteLine (string.Join(" ",f.ListDirectoryEntries("/a/b/c/")));

			Console.WriteLine ("Removing recursively /a/");
			f.RemoveDirectory("/a/", true);

			Console.WriteLine ("Content of / folder:");
			Console.WriteLine (string.Join(" ",f.ListDirectoryEntries("/")));

			Console.WriteLine ("Creating file /dump.dat");
			f.CreateFile("/dump.dat");

			Console.WriteLine ("Content of / folder:");
			Console.WriteLine (string.Join(" ",f.ListDirectoryEntries("/")));

			Console.WriteLine ("Writing to dump.dat");
			byte[] zeroes = new byte[10];
			f.WriteFile("/dump.dat", 0, zeroes);

			Console.WriteLine ("Reading 10 bytes from dump.dat");
			byte[] data = new byte[10];
			f.ReadFile("/dump.dat", 0, data);
			Console.WriteLine (string.Join(" ", data));

			Console.WriteLine ("Removing file dump.dat");
			f.RemoveFile("/dump.dat");

			Console.WriteLine ("Content of / folder:");
			Console.WriteLine (string.Join(" ",f.ListDirectoryEntries("/")));

			Console.WriteLine ("Closing container");
			f.Close();
			Console.WriteLine ("Closing container again");
			f.Close();
		}
	}
}
