using System;
using System.IO;

namespace Cameleonica
{
	public class Extent
	{
		public long Offset;
		public long EndOffset;

		public long Length {
			get { 
				return EndOffset - Offset;
			}
		}

		public Extent ()
		{
			this.Offset = 0;
			this.EndOffset = 0;
		}

		public Extent (long offset, long endoffset)
		{
			if (endoffset < offset) {
				throw new ArgumentException ("Extent constructor requires a valid range which does not end earlier than it starts.");
			}
			this.Offset = offset;
			this.EndOffset = endoffset;
		}

		public Extent (long offset, long endoffset, long length)
		{
			if (length < 0) {
				throw new ArgumentException ("Extent constructor requires a non-negative length.");
			}
			if (endoffset < 0) {
				this.Offset = offset;
				this.EndOffset = offset + length;
				return;
			}
			if (offset < 0) {
				if (endoffset < length) {
					throw new ArgumentException("Extent constructor requires a range that starts at 0 or later.");
				}
				this.Offset = endoffset - length;
				this.EndOffset = endoffset;
				return;
			}
			throw new ArgumentException ("Extent constructor requires arguments like (x,-1,z) or (-1,y,z).");
		}

		public Extent (byte[] raw)
		{
			BinaryReader b = new BinaryReader(new MemoryStream(raw, false));
			this.Offset = b.ReadInt64();
			this.EndOffset = b.ReadInt64();
		}

		public byte[] SaveRaw ()
		{
			BinaryWriter b = new BinaryWriter(new MemoryStream());
			b.Write((Int64)this.Offset);
			b.Write((Int64)this.EndOffset);
			return (b.BaseStream as MemoryStream).ToArray();
		}

		public override string ToString ()
		{
			return string.Format ("{0}..{1} ({2})", Offset, EndOffset, Length);
		}

	}
}

