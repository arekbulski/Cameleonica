#!/usr/bin/python3
import unittest
from keyvaluestore import Container


class TestContainer(unittest.TestCase):

    def setUp(self):
        self.c = Container('/tmp/test-keyvaluestore', overwrite=1)

    def test_set(self):
        self.c.set(1, 2)
        self.c["bykey"] = "value"
        self.assertEqual(self.c.get(1), 2)
        self.assertEqual(self.c["bykey"], "value")

    def test_set_overwrite(self):
        self.c.set(1, 2)
        self.c.set(1, 3)
        self.c.set(1, 4)
        self.assertEqual(self.c.get(1), 4)
