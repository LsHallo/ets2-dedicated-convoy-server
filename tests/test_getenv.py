import os
import unittest

from ets_server_entrypoint import getenv

class TestGetenv(unittest.TestCase):

    def test_is_equals_to_native(self):
        os.environ["TEST"] = "ABC"
        self.assertEqual(getenv("TEST"), os.getenv("TEST"))
        self.assertEqual(getenv("UNDEFINED_VARIABLE_DOES_NOT_EXIST_1239u5qpof"), os.getenv("UNDEFINED_VARIABLE_DOES_NOT_EXIST_1239u5qpof"))

    def test_ats_ets(self):
        os.environ["ETS_TEST"] = "ets"
        os.environ["ATS_TEST"] = "ets"

        self.assertEqual(getenv("ETS_TEST"), getenv("ATS_TEST"))

    def test_default(self):
        os.environ["TEST"] = "ABC"
        self.assertEqual(getenv("UNDEFINED_VARIABLE_DOES_NOT_EXIST_1239u5qpof", "abc"), "abc")
        self.assertEqual(getenv("TEST"), "ABC")

    def tearDown(self):
        os.environ.pop("TEST", None)
        os.environ.pop("ETS_TEST", None)
        os.environ.pop("ATS_TEST", None)
        return super().tearDown()

if __name__ == "__main__":
    unittest.main()