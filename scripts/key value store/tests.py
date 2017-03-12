#!/usr/bin/python3
import unittest
import keyvaluestore


def raises(func, *args, **kw):
    try:
        ret = func(*args, **kw)
    except Exception as e:
        return e.__class__
    else:
        return None


class TestContainer(unittest.TestCase):

    def setUp(self):
        self.container = keyvaluestore.Container('/tmp/keyvaluestore1', overwrite=True)

    def test_set(self):
        c = self.container
        c.removeall()
        c.set(1, 2)
        c['key'] = 'value'
        assert c[1] == 2
        assert c['key'] == 'value'
        assert c[...] == {1:2, 'key':'value'}

    def test_set_overwrite(self):
        c = self.container
        c.removeall()
        c.set(1, 2)
        c.set(1, 3)
        c.set(1, 4)
        assert c[1] == 4
        assert c[...] == {1:4}

    def test_get_missing(self):
        c = self.container
        c.removeall()
        assert raises(lambda: c['missing']) == KeyError
        assert c[...] == {}
        c['missing'] = None
        assert c['missing'] == None
        assert c[...] == {'missing':None}
        del c['missing']
        assert raises(lambda: c['missing']) == KeyError
        assert c[...] == {}

    def test_getvalues():
        c = self.container
        c.removeall()
        c[1] = 2
        assert c[...] == {1:2}

    def test_getvalues():
        c = self.container
        c.removeall()
        c[1] = 2
        assert c[...] == {1:2}
        c.removeall()
        assert c[...] == {}
