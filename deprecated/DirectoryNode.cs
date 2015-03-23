using System;

namespace Cameleonica
{
	public class DirectoryNode
	{
		public string Name {
			get;
			private set;
		}

		public string PathName {
			get;
			private set;
		}

		public FileNode[] Files {
			get;
			private set;
		}

		public DirectoryNode[] Subdirectories {
			get;
			private set;
		}

		public static DirectoryNode RootDirectory {
			get;
			private set;
		}

		public void CreateFile (string filename)
		{
			throw new NotImplementedException();
		}

		public void CreateDirectory (string dirname)
		{
			throw new NotImplementedException();
		}

		public void RemoveFile (string filename)
		{
			throw new NotImplementedException();
		}

		public void RemoveDirectory (string dirname)
		{
			throw new NotImplementedException();
		}

		private DirectoryNode ()
		{
			throw new NotImplementedException();
		}

		static DirectoryNode ()
		{
			throw new NotImplementedException();
		}
	}
}

