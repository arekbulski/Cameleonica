#!/usr/bin/python3
import keyvaluestore


def throws(code, errortype):
    try:
        code()
    except errortype, e:
        return True
    else:
        return False

assert throws(lambda: 1, AssertionError)
assert throws(lambda: open('???'), OSError)


filename = '/tmp/test-keyvaluestore'

with keyvaluestore.Container(filename) as c:
    assert c.getkeys() == []
    c.set(1, 2)
    assert c.get(1) == ('any picklable object', 2)
    assert c.get('nonexisting') == None
    assert c.getkeys() == [1]
    c.revert()
    assert c.getkeys() == []

