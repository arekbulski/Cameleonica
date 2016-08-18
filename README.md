  Cameleonica filesystem
==========================

Cameleonica is a safe cryptographic steganographic advanced filesystem. It aims to guarantee confidentiality, authenticity, plausible deniability, transactions, snapshots, versioning, instantaneous copying, permanent deletion, high performance, low delays, reliability, compression, and hashing.

Further design will include a FUSE and Dokan frontend, and a Nautilus extension. A graphical interface will also be provided if a filesystem driver is too much. Secure cryptographic schemes will be used such as AES-GCM and ChaCha20-Poly1305 authenticated encryption, Keccak and SipHash hashing, scrypt password-based key derivation, /dev/urandom and CryptGenRandom random generators. Design will include extents, complete inodes, copy on write, log structured segments layout, intent based recovery, and deniably encrypted pointers. Deterministic compilation with Bazel may be used to release binaries. 

  Project status and roadmap
------------------------------

Only design documentation is being developed at this point. You can help by reviewing these documents and posting questions and suggestions for improvement. Easiest way for you to ask questions is to create a new Issue. 

- [complete document](documentation/combined.pdf) (42 pages)

Documentation is divided into sections:

- Mission statement (10 pages)
- Ideas and Observations (20 pages)
- Preliminary design (8 pages)
- Questions and Answers (4 pages)

Experimental code is also in the repository.

  Development notice
----------------------

Code will be developed in Python and later also in the kernel (a long way ahead). Documentation is created in LibreOffice, XMind and [draw.io](https://www.draw.io/). User experience design will later be done in Glade.

License is set to MIT Licence, unless something changes.

