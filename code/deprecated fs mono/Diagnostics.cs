using System;
using System.Diagnostics;

namespace Cameleonica
{
	public static class Diagnostics
	{
		static Diagnostics ()
		{
		}

		public static TimeSpan TimeIt (Action action)
		{
			Stopwatch s = Stopwatch.StartNew();
			action.Invoke();
			return s.Elapsed;
		}

	}
}

