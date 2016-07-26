#!/usr/bin/python3
import keyvaluestore

c = keyvaluestore.Container("/tmp/test-keyvaluestore")
assert c.getkeys() == []
c.set(1, 2)
assert c.get(1) == ("any picklable object", 2)
assert c.get("nonexisting") == None
assert c.getkeys() == [1]
c.revert()
assert c.getkeys() == []
