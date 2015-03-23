using System;
using System.IO;

namespace Cameleonica
{
	public static class RawSerializer
	{
		public static byte[] SaveRaw (Action<BinaryWriter> writer)
		{
			MemoryStream m = new MemoryStream ();
			BinaryWriter b = new BinaryWriter (m);
			writer.Invoke (b);
			return m.ToArray ();
		}

		public static void LoadRaw (byte[] rawdata, Action<BinaryReader> reader)
		{
			MemoryStream m = new MemoryStream (rawdata, false);
			BinaryReader b = new BinaryReader (m);
			reader.Invoke (b);
		}

	}
}
