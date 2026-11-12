import unittest

from tags import normalize_tag


class NormalizeTagTests(unittest.TestCase):
    def test_normalize_tag_contract(self):
        for value, expected in (("  Blue  ", "Blue"), (" 茶 ", "茶")):
            with self.subTest(value=value):
                self.assertEqual(normalize_tag(value), expected)

        for value in ("", " \t\n"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError) as error:
                    normalize_tag(value)
                self.assertEqual(str(error.exception), "tag required")


if __name__ == "__main__":
    unittest.main()
