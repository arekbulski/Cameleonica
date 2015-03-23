using System;
using System.IO;
using System.Collections.Generic;

namespace Cameleonica
{
	public class CryptoContainer
	{
		private static FileStream randombits;
		private static FileStream zerobits;

		static CryptoContainer ()
		{
			randombits = new FileStream("/dev/urandom", FileMode.Open);
			zerobits = new FileStream("/dev/zero", FileMode.Open);
		}

		private FileStream container;
		private long nextfreeoffset;

		public CryptoContainer (string container)
		{
			this.container = new FileStream(container, FileMode.Open, FileAccess.ReadWrite, FileShare.None);
			this.nextfreeoffset = 128;
			/// HACK: NextFreeOffset is reset to some number at mount. Content will turn to shit.
		}

		~CryptoContainer ()
		{
			this.Close();
		}

		public void Close ()
		{
			this.container.Flush(true);
			this.container.Close();
		}

		public static void CreateContainer (string container, long requestedsize = -1)
		{
			using (FileStream f = new FileStream(container, FileMode.OpenOrCreate, FileAccess.ReadWrite, FileShare.None)) {
			
				if (requestedsize > 0) {
					f.SetLength (requestedsize);
				}
				if (f.Length < Const.MinContainerSize) {
					throw new Exception (string.Format(
						"Failed to create container with size {0} bytes, minimum is {1} bytes.", 
                       	requestedsize, Const.MinContainerSize ));
				}

				byte[] buf = new byte[64000];
				f.Position = 0;
				while (f.Position < f.Length) {
					int more = Math.Min (buf.Length, (int)(f.Length - f.Position));
					randombits.Read (buf, 0, more);
					f.Write (buf, 0, more);
				}

				f.Position = 0;
				byte[] rootpointer = new Extent (64, 128).SaveRaw ();
				f.Write (rootpointer, 0, rootpointer.Length);
				zerobits.Read (buf, 0, 512);
				f.Write (buf, 0, 512);
			}
		}

		public void FormatContainer ()
		{
			/// UNDONE: Instead of creating containers, just mount them with no password, then format them.
		}

		public void ChangePassphrases (byte[][] pass)
		{
			/// UNDONE: If you know how many keys you use, you can set new passwords for them.
		}

		public bool DirectoryExists (string pathname)
		{
			throw new NotImplementedException();
		}

		public string[] ListDirectoryEntries (string pathname)
		{
			InodeExtent parent = open(pathname);

			string[] result = new string[parent.Content.Count];
			for (int i = 0; i < result.Length; i++) {
				InodeExtent e = new InodeExtent(loadraw(parent.Content[i]));
				result[i] = e.Name + (e.IsPlainFile ? "" : "/");
			}
			return result;
		}

		public void CreateDirectory (string pathname)
		{
			open(pathname +"/", true);
		}

		public void RemoveDirectory (string pathname, bool recursive = false)
		{
			InodeExtent removed = open(pathname +"/");
			/// UNDONE: Ending slash is ignored when opening inode.

			if (recursive == false) {
				if (removed.IsPlainFile) {
					throw new ArgumentException("Failed to remove directory, name points to a file.");
				}
				if (removed.Content.Count > 0) {
					throw new ArgumentException("Failed to remove non-empty directory. Try recursive removal?");
				}
			}

			InodeExtent last = removed.Parent;

			if (last == null) {
				saveraw(new InodeExtent(false,"").SaveRaw(), last.Address);
			} else {
				last.Content.Remove(removed.Address);
				saveraw(last.SaveRaw(), last.Address);
			}
		}

		public void CopyDirectory (string pathname, string newpathname)
		{
			throw new NotImplementedException();
		}

		public void MoveDirectory (string pathname, string newpathname)
		{
			throw new NotImplementedException();
		}

		public void RenameDirectory (string pathname, string newname)
		{
			throw new NotImplementedException();
		}

		public bool FileExists (string pathname)
		{
			throw new NotImplementedException();
		}

		public void CreateFile (string pathname)
		{
			open(pathname, true);
		}

		public void RemoveFile (string pathname)
		{
			InodeExtent file = open(pathname);
			if (file.IsPlainFile == false) {
				throw new ArgumentException("Failed to remove file, name points to a directory.");
			}

			InodeExtent last = file.Parent;
			int q = last.Content.LastIndexOf(file.Address);

			last.Content.RemoveAt(q);
			saveraw(last.SaveRaw(), last.Address);
		}

		public void CopyFile (string pathname, string newpathname)
		{
			throw new NotImplementedException();
		}

		public void MoveFile (string pathname, string newpathname)
		{
			throw new NotImplementedException();
		}

		public void RenameFile (string pathname, string newname)
		{
			throw new NotImplementedException();
		}

		public void ReadFile (string pathname, long position, byte[] buffer, long offset = 0, long length = -1)
		{
			InodeExtent file = open(pathname);

			if (length < 0) {
				length = buffer.Length;
			}
			long past = 0;
			long stored = 0;
			foreach (var e in file.Content) {
				if (past+e.Length < position) {
					past += e.Length;
					continue;
				}
				if (past >= position+length) {
					break;
				}
				long a = position-past;
				long b = Math.Min(e.Length, length-stored);

				container.Position = e.Offset+a;
				container.Read(buffer, (int)stored, (int)b);
				stored += b;
				past += e.Length;
			}
			if (stored < length) {
				throw new Exception("Failed to read complete buffer, file was too short.");
			}
		}

		public void WriteFile (string pathname, long position, byte[] buffer, int offset = 0, int length = -1)
		{
			InodeExtent file = open(pathname);
			InodeExtent last = file.Parent;
			int q = last.Content.LastIndexOf(file.Address);
			
			if (length < 0) {
				length = buffer.Length;
			}
			Extent newdata = allocateraw(length);
			container.Position = newdata.Offset;
			container.Write(buffer, offset, length);

			file.Content.Add(newdata);
			/// UNDONE: Bug, content is always added to the end of file.

			Extent filepointer = saveraw(file.SaveRaw());
			last.Content[q] = filepointer;
			saveraw(last.SaveRaw(), last.Address);
		}

		public ulong GetFileSize (string pathname)
		{
			throw new NotImplementedException();
		}

		public void SetFileSize (string pathname, ulong length)
		{
			throw new NotImplementedException();
		}

		public string GetFileAttributes (string pathname)
		{
			throw new NotImplementedException();
		}

		public void SetFileAttributes (string pathname, string newattributes)
		{
			throw new NotImplementedException();
		}

		private byte[] loadraw (Extent area)
		{
			byte[] buf = new byte[area.Length];
			container.Position = area.Offset;
			container.Read(buf, 0, buf.Length);
			return buf;
		}

		private Extent allocateraw (long requestedlength)
		{
			Extent allocated = new Extent(nextfreeoffset, -1, requestedlength);
			nextfreeoffset += requestedlength;
			return allocated;
		}

		private Extent saveraw (byte[] raw, Extent allocated = null)
		{
			if (allocated == null) {
				allocated = allocateraw(raw.Length);
			} 
			if (allocated.Length < raw.Length) {
				throw new Exception("Failed to write raw extent, allocated area is too small.");
			}
			container.Position = allocated.Offset;
			container.Write(raw, 0, raw.Length);
			return allocated;
		}

		private InodeExtent open (string pathname, bool create = false)
		{
			string[] parts = pathname.Split(new char[]{'/'}, StringSplitOptions.RemoveEmptyEntries);
			bool endsdir = pathname.EndsWith("/");

			Extent pointer = new Extent(loadraw(new Extent(0,64)));
			InodeExtent last = new InodeExtent(loadraw(pointer));
			last.Parent = null;
			last.Address = pointer;

			for (int i = 0; i < parts.Length; i++) {
				if (last.IsPlainFile) {
					throw new DirectoryNotFoundException();
					/// UNDONE: If mid-path directory happens to be a file, fail.
				}
				for (int j = 0; j < last.Content.Count; j++) {
					pointer = last.Content[j];
					InodeExtent sub = new InodeExtent(loadraw(pointer));
					if (sub.Name == parts[i]) {
						sub.Address = pointer;
						sub.Parent = last;
						last = sub;
						goto next;
					}
				}
				if (create) {
					bool plainfile = (i == parts.Length-1 && endsdir == false);
					InodeExtent empty = new InodeExtent(plainfile, parts[i]);
					empty.Parent = last;
					empty.Address = saveraw(empty.SaveRaw());

					last.Content.Add(empty.Address);
					InodeExtent pre = last.Parent;

					if (pre == null) {
						pointer = saveraw(last.SaveRaw());
						saveraw(pointer.SaveRaw(), new Extent(0,64));
					} else {
						int p = pre.Content.LastIndexOf(last.Address);
						pointer = saveraw(last.SaveRaw());
						pre.Content[p] = pointer;
						saveraw(pre.SaveRaw(), pre.Address);
					}
					last = empty;

					goto next;
				}
				throw new DirectoryNotFoundException();

				next: 
					continue;
			}

			if (last.IsPlainFile == endsdir) {
				throw new ArgumentException(string.Format("Failed to open a {0}, name points to a {1}.",
				                            endsdir ? "directory" : "file", 
				                            last.IsPlainFile ? "file" : "directory"));
			}
			return last;
		}

	}
}
