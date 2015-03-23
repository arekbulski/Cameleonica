using System;

namespace Cameleonica
{
	/// Constants are defined in units of 1024^n bytes, where n=0,1,... is B,KB,MB,GB,...
	/// 
	public static class Const
	{
		public const long Sector = 512;       /// 512 B
		public const long Block =  4   *1024; /// 4 KB

		public const long MinContainerSize = 1L  *1024 *1024;       /// 1 MB
		public const long PreallocateReady = 10L *1024 *1024 *1024; /// 10 GB
	}
}
