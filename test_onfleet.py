#!/usr/bin/env python

import unittest

class TestOnfleetAPI(unittest.TestCase):
    def setUp(self):
        pass

    def test_example(self):
        assert(2 + 2 == 4)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOnfleetAPI)
    unittest.TextTestRunner(verbosity=2).run(suite)

