
  Cameleonica filesystem
==========================

Cameleonica is a prototype safe cryptographic steganographic advanced filesystem.

Features include confidentiality, authenticity, plausible deniability, permanent deletion, versioning, snapshots, atomicity, transactions, file and directory cloning, internal compression, non-transparent compression and hashing, deduplication, serializability, multiple-device replication and tiering. 

Internal design includes atomic and ordered operations, diskless fsync, copy on write, segmented log-structured disk layout, copying garbage collector, complete inodes, complete dictionary, rings and chains abstract data structures, file-level replication and tiering. 

  Project status and roadmap
------------------------------

Only design documentation is being developed at this point. You can help by reviewing these documents and posting questions or suggestions for improvement, just create a new Issue. Please do NOT submit Pull Requests, unless recording changes was enabled. It is impossible to diff odt files.

- [Complete specification pdf](documentation/combined.pdf) (48 pages)

Documentation is divided into sections:

- Mission statement (6 pages)
- Ideas and Observations (20 pages)
- Preliminary design (currently edited, 10 pages)
- Python/Fuse implementation plan (currently edited, 6 pages)
- Questions and Answers (4 pages)

Experimental code is also in the repository.

  Development notice
----------------------

Code will be developed in Python/FUSE and later possibly in-kernel. Documentation is created in LibreOffice, XMind and [draw.io](https://www.draw.io/). User experience design will be done in Glade.

License is set to MIT Licence, unless something changes.
