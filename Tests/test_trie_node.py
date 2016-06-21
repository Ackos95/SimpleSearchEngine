__author__ = 'Acko'

import unittest

from trie.trie import TrieNode


class MyTestCase(unittest.TestCase):

    def test_trie_node_create_wrong_param(self):
        with self.assertRaises(TypeError):
            TrieNode(12)

        with self.assertRaises(TypeError):
            TrieNode(True)

        with self.assertRaises(TypeError):
            TrieNode("A", parent="a")

        with self.assertRaises(TypeError):
            TrieNode("A", parent=123)

    def test_trie_node_create_right_param(self):
        t = TrieNode("A")
        self.assertEqual(t.get_key(), "A")
        self.assertEqual(t.get_parent(), None)
        self.assertTrue(isinstance(t, TrieNode))

        t1 = TrieNode("b", parent=t)
        self.assertEqual(t1.get_key(), "b")
        self.assertEqual(t1.get_parent(), t)
        self.assertEqual(t1.get_parent().get_key(), t.get_key())

        self.assertTrue(t.has_child("b"))
        self.assertFalse(t.has_child("A"))
        self.assertEqual(t["b"], t1)

    def test_trie_node_end(self):
        t = TrieNode("A", end=True)
        t1 = TrieNode("B")

        self.assertTrue(t.is_end())
        self.assertFalse(t1.is_end())

        t1.set_end()
        self.assertTrue(t1.is_end())

        # Just to show that nothing changes, it wont turn again in False
        t.set_end()
        self.assertTrue(t.is_end())

    def test_trie_node_data(self):
        t = TrieNode("A", data="Some random data")
        t1 = TrieNode("B")

        self.assertTrue(t.has_data())
        self.assertEqual(t.get_data(), "Some random data")
        self.assertFalse(t1.has_data())

        t1.set_data(123)
        self.assertTrue(t1.has_data())
        self.assertEqual(t1.get_data(), 123)

        t.set_data(t1)
        self.assertTrue(t.has_data())
        self.assertEqual(t.get_data(), t1)
        self.assertEqual(t.get_data().get_data(), t1.get_data())



if __name__ == '__main__':
    unittest.main()
