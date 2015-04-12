  Cameleonica filesystem
==========================

Cameleonica is a **safe cryptographic steganographic advanced filesystem**. It aims to guarantee confidentiality, authenticity, plausible deniability, transactions, snapshots and versioning, instantaneous copying, permanent deletion, high performance and low delays, compression, and hashing.

Further design will include a FUSE frontend and Nautilus extension. A graphical interface will also be provided where a filesystem driver may not be possible to implement (Windows). Secure cryptographic schemes will be used such as AES-GCM and ChaCha20-Poly1305 authenticated encryption, SHA-3 and scrypt, /dev/urandom and CryptGenRandom. Internally extents, complete inodes, copy on write, ring buffers of discrete updates, and deniably encrypted pointers will be used.

  Project status and roadmap
------------------------------

Project is under heavy work right now. Design documentation is the main focus and it will stay that way for several months. Right now, goals are better defined than means of achieving them but that will slowly change. I highly recommend reading:

- [Mission statement](documentation/mission.pdf) (6 pages)

There is no code yet. Further designs will be written down before anything runnable is created. 

  Development notice
----------------------

Code will be developed in Python/Cython. Documentation is created in LibreOffice writer and XMind mind mapping tool. User experience design is done in Glade.

Referenced documentation is a local copy of published material, a good read saved for future need. There are also some random notes, you can just ignore them. Deprecated C# code was put away but kept for reference. It will be removed in the future when real code is more mature. 

License is set to MIT Licence, unless something changes.

  How to contribute
---------------------

Easiest way for you to submit anything is to create a new Issue. GitHub account is all you need for that. No special access to repository is needed.

If you want to just ask a question, feel free to open an Issue as well. I will mark it as such and close it after you are satisfied with answers.

Pull requests and patches are also welcomed if you want to submit some code.

