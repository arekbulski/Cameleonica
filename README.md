  Cameleonica filesystem
==========================

Cameleonica is a **safe cryptographic steganographic advanced filesystem.** It aims to guarantee **confidentiality, authenticity, plausible deniability,
transactions, snapshots and versioning, instantaneous copying, permanent
deletion, high performance and low delays, compression, and hashing.**

Further design will include a FUSE frontend and Nautilus extension. Secure cryptographic schemes will be used, such as AES 256bit, Salsa20, SHA-512, SHA-3, CTR mode, GCM authenticated encryption, /dev/urandom. Internally, extents, copy on write, deniably encrypted pointers will be used.

  Development notice
----------------------

Project will remain in EXPERIMENTAL phase for several months. Please be patient, there will be more documentation published as time goes by. So far you can read:

- [Mission statement](https://github.com/arekbulski/Cameleonica/blob/master/mission.pdf)

Code will be developed in Python/Cython. Documentation is created in LibreOffice and XMind mind mapping tool. 
Deprecated C# code was put away but kept for reference. It will be removed in the future when real code is more mature.

Git rebase may happen during development.

License is set to MIT Licence, unless there will be a reason to change it.

