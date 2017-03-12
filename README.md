  Cameleonica filesystem
==========================

Cameleonica is a safe cryptographic steganographic advanced filesystem.

It aims to guarantee confidentiality, authenticity, plausible deniability, transactions, snapshots, versioning, instantaneous copying, permanent deletion, high throughput, low delays, internal compression, non-transparent compression and hashing, deduplication, departitioning, and serializability.

Internal design includes atomic and ordered operations, diskless fsync, extents, complete inodes, copy on write, segmented log structured disk layout, append only operations, copying garbage collector, complete dictionary and alternative B-tree, rings and chains abstract data structures, file level RAID modes.

  Project status and roadmap
------------------------------

Only design documentation is being developed at this point. You can help by reviewing these documents and posting questions and suggestions for improvement, just create a new Issue.

- [Complete specification pdf](documentation/combined.pdf) (42 pages)
- [First implementation pdf](documentation/implementation2017.pdf) (4 pages)

Documentation is divided into sections:

- Mission statement (8 pages)
- Ideas and Observations (20 pages)
- Preliminary design (being edited, 10 pages)
- Questions and Answers (4 pages)

Experimental code is also in the repository.

  Development notice
----------------------

Code will be developed in Python/Fuse and later also in the Linux kernel or Rust/Fuse (a long way ahead). Documentation is created in LibreOffice, XMind and [draw.io](https://www.draw.io/). User experience design will later be done in Glade.

License is set to MIT Licence, unless something changes.
