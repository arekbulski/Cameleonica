  Cameleonica filesystem
==========================

Cameleonica is a safe cryptographic steganographic advanced filesystem. It aims to guarantee confidentiality, authenticity, plausible deniability, transactions, snapshots, versioning, instantaneous copying, permanent deletion, high performance, low delays, compression, and hashing.

Further design will include a FUSE/Dokan frontend and Nautilus extension. A graphical interface will also be provided if a filesystem driver is too much. Secure cryptographic schemes will be used such as AES-GCM and ChaCha20-Poly1305 authenticated encryption, Keccak and SipHash hashing, scrypt password-based key derivation, /dev/urandom and CryptGenRandom random generators. Design will include extents, complete inodes, copy on write, log structured layout, and deniably encrypted pointers. Deterministic compilation with Bazel may be used to release binaries. 

  Project status and roadmap
------------------------------

Only design documentation is being developed at this point. You can help by reviewing these documents and posting suggestions for improvements. Easiest way for you to submit anything is to create a new Issue or Pull Request. If you want to ask a question or suggest some idea, just open an Issue and post your thing. I will take over from there.

- [Mission statement](documentation/mission.pdf) (7 pages)
- [Questions and Answers](documentation/responses.pdf) (3 pages)
- [Ideas and Observations](documentation/ideas.pdf) (12 pages)

  Development notice
----------------------

Code will be developed in .NET/Mono and later also in the kernel. Documentation is created in LibreOffice and XMind. User experience design will be done in Glade.

License is set to MIT Licence, unless something changes.
