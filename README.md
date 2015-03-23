  Cameleonica filesystem
==========================

It is a managed implementation of a **safe cryptographic steganographic advanced filesystem** with a file/partition backend and Fuse/Gtk frontend. It aims to guarantee confidentiality, integrity, plausible deniability on per-password basis, directories containing different-password entities, weak or strong ACID transaction properties, read-only snapshots of selected directories, instantaneous copying of files. Secure cryptographic schemes will be used, such as AES 256bit, SHA-512, CTR and LRW modes, PMAC, /dev/urandom, Salsa20, RIPEM-D, SHA-3. Internally, extents, copy on write, deniably encrypted pointers will be used.

  Development notice
----------------------

Project will remain in EXPERIMENTAL phase for several months. Please be patient, there will be more documentation on planned features posted on the project site. At this point, this projects is just a messy idea in my head.

Current C# code (Mono.Fuse) will possibly be discarded and replaced with new Python/Cython code (python-fuse) in the future. The decision to switch to Python has not been made yet.

Git rebase may happen during initial days of development.

License is set to MIT Licence, until a more permanent decision be made.
