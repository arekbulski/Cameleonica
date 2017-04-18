

Offtopic. If you would like to check out my newest creation, please enjoy. :smile:

This is a ~2h video course with programming assignments teaching filesystem internals,
some of which are actually taken from this project.
https://stepik.org/course/Applied-Computer-Science-Filesystems-internals-2475

You can also support me on Patreon:
https://www.patreon.com/cameleonica


  Cameleonica filesystem
==========================

Cameleonica is a prototype safe cryptographic steganographic advanced filesystem.

It aims to guarantee confidentiality, authenticity, plausible deniability, permanent deletion, versioning, snapshots, transactions, directory cloning, high throughputs, low delays, internal compression, non-transparent compression and hashing, deduplication, departitioning, serializability, multiple-device replication and tiering.

Internal design includes atomic and ordered operations, diskless fsync, extents, complete inodes, copy on write, segmented log structured disk layout, append only operations, copying garbage collector, complete dictionary and alternative B-tree, rings and chains abstract data structures, file level RAID modes.

  Project status and roadmap
------------------------------

Only design documentation is being developed at this point. You can help by reviewing these documents and posting questions or suggestions for improvement, just create a new Issue.

- [Complete specification pdf](documentation/combined.pdf) (42 pages)
- [First implementation pdf](documentation/implementation2017.pdf) (currently edited, 6 pages)

Documentation is divided into sections:

- Mission statement (8 pages)
- Ideas and Observations (currently edited, 20 pages)
- Preliminary design (currently edited, 10 pages)
- Questions and Answers (4 pages)

Experimental code is also in the repository.

  Development notice
----------------------

Code will be developed in Python/Fuse and later also in the Linux kernel or Rust/Fuse (a long way ahead). Documentation is created in LibreOffice, XMind and [draw.io](https://www.draw.io/). User experience design will later be done in Glade.

License is set to MIT Licence, unless something changes.
