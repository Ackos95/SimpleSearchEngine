# -*- coding: utf-8 -*-
__author__ = 'Acko'

import unittest
from trie.trie import Trie


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.trie = Trie()
        self.trie.add_word("Test")
        self.trie.add_word("asdf")
        self.trie.add_word("foo")

    def tearDown(self):
        self.trie = None

    def test_find_word(self):
        self.assertTrue(self.trie.has_word("Test"))
        self.assertTrue(self.trie.has_word("asdf"))
        self.assertTrue(self.trie.has_word("foo"))

    def test_find_word_fail(self):
        self.assertFalse(self.trie.has_word("aaaa"))
        self.assertFalse(self.trie.has_word("Tests"))
        self.assertFalse(self.trie.has_word("Tes"))

    def test_find_word_ignoreCase(self):
        self.assertTrue(self.trie.has_word("TEST"))
        self.assertTrue(self.trie.has_word("test"))
        self.assertTrue(self.trie.has_word("ASDF"))
        self.assertTrue(self.trie.has_word("FOO"))

    def test_find_word_caseSensitive(self):
        self.assertFalse(self.trie.has_word("TEST", ignore_case=False))
        # True because "Test" was added with ignore_case on  default true parameter
        self.assertTrue(self.trie.has_word("test", ignore_case=False))
        # False same as top ("Test" word was added with ignore_case on default true)s
        self.assertFalse(self.trie.has_word("Test", ignore_case=False))
        self.assertFalse(self.trie.has_word("ASDF", ignore_case=False))
        self.assertFalse(self.trie.has_word("FOO", ignore_case=False))

    def test_add_word(self):
        self.trie.add_word("newOne")
        self.trie.add_word("асдф")
        self.assertTrue(self.trie.has_word("newOne"))
        self.assertTrue(self.trie.has_word("newone"))
        self.assertTrue(self.trie.has_word("NEWONE"))
        self.assertFalse(self.trie.has_word("newOnes"))

    def test_add_word_caseSensitive(self):
        self.trie.add_word("FirstOne", ignore_case=False)
        self.assertFalse(self.trie.has_word("FirstOne"))  # False because ignore_case in search is default true
        self.assertTrue(self.trie.has_word("FirstOne", ignore_case=False))
        self.assertFalse(self.trie.has_word("firstone", ignore_case=False))
        self.assertFalse(self.trie.has_word("FIRSTONE", ignore_case=False))

    def test_get_node(self):
        self.assertIsNone(self.trie.get_node("AAAAAA"))
        self.assertEqual(self.trie.get_node("test").get_key(), "t")
        self.assertEqual(self.trie.get_node("tes").get_key(), "s")
        self.assertEqual(self.trie.get_node("te").get_parent().get_key(), "t")
        self.assertEqual(self.trie.get_node("t").get_parent().get_key(), "__root__")


if __name__ == '__main__':
    unittest.main()
