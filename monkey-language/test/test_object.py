import monkey.object as obj
import unittest


class TestObject(unittest.TestCase):

    def test_string_hash_key(self):
        hello1 = obj.String("Hello World")
        hello2 = obj.String("Hello World")
        diff1 = obj.String("My name is johnny")
        diff2 = obj.String("My name is johnny")

        self.assertEqual(hello1.hash_key().value, hello2.hash_key().value,
                         "strings with same content have different hash keys")
        self.assertEqual(diff1.hash_key().value, diff2.hash_key().value,
                         "strings with same content have different hash keys")
        self.assertNotEqual(hello1.hash_key().value, diff1.hash_key().value,
                            "strings with different content have same hash keys")
