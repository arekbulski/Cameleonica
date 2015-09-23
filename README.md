  Cameleonica filesystem
==========================

Cameleonica is a safe cryptographic steganographic advanced filesystem. It aims to guarantee confidentiality, authenticity, plausible deniability, transactions, snapshots, versioning, instantaneous copying, permanent deletion, high performance, low delays, compression, and hashing.

Further design will include a FUSE/Dokan frontend and Nautilus extension. A graphical interface will also be provided if a filesystem driver is too much. Secure cryptographic schemes will be used such as AES-GCM and ChaCha20-Poly1305 authenticated encryption, Keccak and SipHash hashing, scrypt key derivation, /dev/urandom and CryptGenRandom random generators. Design will include extents, complete inodes, copy on write, ring buffers, and deniably encrypted pointers will be used. Deterministic compilation with Bazel may be used to release binaries. 

  Project status and roadmap
------------------------------

Project is "under construction". Design documentation is the main focus right now, and there will be no code to back it up for months. Gedunken experiments is what is being run. I highly recommend reading:

- [Mission statement](documentation/mission.pdf) (7 pages)
- [Questions and Answers](documentation/responses.pdf) (3 pages)
- [Ideas and Observations](documentation/ideas.pdf) (12 pages)

If you want to help, read these and post a review.

  Development notice
----------------------

Code will be developed in .NET/Mono and later also in kernel. Documentation is created in LibreOffice and XMind. User experience design will be done in Glade.

Referenced documentation is a local copy of published articles. All bibliography entries (and few more unmentioned) are there. There are also some random notes, few wallpapers, and other junk you can ignore.

License is set to MIT Licence, unless something changes.

  How to contribute
---------------------

Easiest way for you to submit anything is to create a new Issue. GitHub account is all you need for that. No special access to repository is needed. If you want to ask a question or suggest some idea, just open an Issue and post your thing. I will take over from there.

What can you do? Most valuable work you can do is review the documents. Poke a hole in them, show they are missing something important, provide counter-arguments. 
