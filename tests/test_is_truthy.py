import unittest

from ets_server_entrypoint import is_truthy


class TestIsTruthy(unittest.TestCase):

    def test_truthy_values(self):
        self.assertTrue(is_truthy("true"))
        self.assertTrue(is_truthy("TRUE"))
        self.assertTrue(is_truthy(" True "))
        self.assertTrue(is_truthy("yes"))
        self.assertTrue(is_truthy("YES"))
        self.assertTrue(is_truthy("on"))
        self.assertTrue(is_truthy("ON"))
        self.assertTrue(is_truthy("1"))

    def test_falsey_values(self):
        self.assertFalse(is_truthy(None))
        self.assertFalse(is_truthy(""))
        self.assertFalse(is_truthy(" "))
        self.assertFalse(is_truthy("false"))
        self.assertFalse(is_truthy("False"))
        self.assertFalse(is_truthy("no"))
        self.assertFalse(is_truthy("off"))
        self.assertFalse(is_truthy("0"))
        self.assertFalse(is_truthy("random"))

    def test_non_string_values(self):
        self.assertTrue(is_truthy(True))
        self.assertFalse(is_truthy(False))
        self.assertTrue(is_truthy(1))
        self.assertFalse(is_truthy(0))
        self.assertFalse(is_truthy([]))
        self.assertFalse(is_truthy({}))


if __name__ == "__main__":
    unittest.main()