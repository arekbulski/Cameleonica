
  Cameleonica filesystem
==========================

Cameleonica is a prototype safe cryptographic steganographic advanced filesystem.

Features include integrity, versioning, snapshots, atomicity, transactions, confidentiality, authenticity, permanent deletion, plausible deniability, file and directory cloning, internal compression, integration of compression and hashing, serializability, file-level replication and tiering. 

(*) Internal design includes atomic and ordered operations, diskless fsync, copy on write, segmented log-structured disk layout, copying garbage collector, complete inodes, complete dictionary, rings and chains abstract data structures, file-level replication and tiering. (*)

  Project status and roadmap
------------------------------

Only design documentation is being developed at this point. You can help by reviewing the combined document and posting questions or suggestions for improvement. Just create a new GitHub Issue.

- [Complete specification pdf](documentation/combined.pdf) (48 pages)

Implementation effort should start with the beginning of 2022. Wish me luck.
