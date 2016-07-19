using System;
using System.IO;
using System.Collections.Generic;

namespace Cameleonica
{
	public class InodeExtent
	{
		public bool IsPlainFile;
		public string Name;
		public List<Extent> Content;

		public Extent Address;
		public InodeExtent Parent;

		public InodeExtent ()
		{
			throw new NotImplementedException();
		}

		public InodeExtent (bool plainfile, string name)
		{
			IsPlainFile = plainfile;
			Name = name;
			Content = new List<Extent>();
		}

		public InodeExtent (byte[] raw)
		{
			BinaryReader b = new BinaryReader(new MemoryStream(raw, false));
			IsPlainFile = b.ReadBoolean();
			Name = b.ReadString();
			Content = new List<Extent>();
			int count = b.ReadInt32();
			for (int i = 0; i < count; i++) {
				Content.Add(new Extent(b.ReadInt64(), b.ReadInt64()));
			}
		}

		public byte[] SaveRaw ()
		{
			BinaryWriter b = new BinaryWriter(new MemoryStream());
			b.Write((bool)IsPlainFile);
			b.Write((string)Name);
			b.Write((Int32)Content.Count);
			foreach (Extent e in Content) {
				b.Write((Int64)e.Offset);
				b.Write((Int64)e.EndOffset);
			}
			return (b.BaseStream as MemoryStream).ToArray();
		}

		public override string ToString ()
		{
			return string.Format ("\"{0}\" {1} with {2} entries", this.Name, 
			                      this.IsPlainFile ? "file" : "directory", 
			                      this.Content.Count);
		}



	}
}

