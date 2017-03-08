  Cameleonica filesystem
==========================

Cameleonica is a prototype of a highly versatile filesystem and is to cover a wide range of safety and security and usability features. It aims to guarantee confidentiality, authenticity, plausible deniability, transactions, snapshots, versioning, instantaneous copying, permanent deletion, high performance, low delays, non-transparent compression and hashing, and manageability. 

Internal design includes extents, complete inodes, copy on write, atomic and ordered operations, segmented log structured layout. Possibly also intent based recovery, and deniably encrypted pointers. 

  Project status and roadmap
------------------------------

Only design documentation is being developed at this point. You can help by reviewing these documents and posting questions and suggestions for improvement, just create a new Issue. 

- [Complete specification pdf](documentation/combined.pdf) (44 pages)
- [First implementation pdf](documentation/implementation2017.pdf) (4 pages)

Documentation is divided into sections:

- Mission statement (10 pages)
- Ideas and Observations (20 pages)
- Preliminary design (being edited, 10 pages)
- Questions and Answers (4 pages)

Experimental code is also in the repository.

  Development notice
----------------------

Code will be developed in Python/Fuse and later also in the Linux kernel or Rust/Fuse (a long way ahead). Documentation is created in LibreOffice, XMind and [draw.io](https://www.draw.io/). User experience design will later be done in Glade.

License is set to MIT Licence, unless something changes.

