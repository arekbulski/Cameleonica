using System;

namespace Cameleonica
{
	public static class Binary
	{
		public static long KB (long n)
		{
			return n *1024;
		}

		public static long MB (long n)
		{
			return n *1024 *1024;
		}

		public static string ToString (long bytes)
		{
			long n = 0;
			long b = bytes;
			while (b >= 1024) {
				n++;
				b /= 1024;
			}

			string[] suffix = new string[]{" B"," KB"," MB"," GB"," TB"};
			return b.ToString() + suffix[n];
		}

	}
}
