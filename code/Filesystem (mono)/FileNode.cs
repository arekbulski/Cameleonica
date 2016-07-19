using System;

namespace Cameleonica
{
	public class FileNode
	{
		public string Name {
			get;
			set;
		}

		public string PathName {
			get;
			set;
		}

		public ulong SizeInBytes {
			get;
			set;
		}

		public string Attributes {
			get;
			set;
		}

		private FileNode ()
		{
			throw new NotImplementedException();
		}
	}
}

