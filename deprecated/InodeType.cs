using System;

namespace Cameleonica
{
	public enum InodeType : byte
	{
		Unspecified = 0,
		File = 1, 
		Directory = 2,
		SymbolicLink = 3,
		Journal = 4,
		Profile = 5,
	}
}

