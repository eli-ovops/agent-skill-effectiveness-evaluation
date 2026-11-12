import unittest

from tags import normalize_tag


class NormalizeTagTests(unittest.TestCase):
    def test_preserves_case_and_chinese_after_trimming(self):
        for value, expected in (("  Blue  ", "Blue"), (" 茶 ", "茶")):
            with self.subTest(value=value):
                self.assertEqual(normalize_tag(value), expected)

    def test_rejects_empty_and_whitespace_only_tags(self):
        for value in ("", " \t\n "):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, r"\Atag required\Z"):
                    normalize_tag(value)


if __name__ == "__main__":
    unittest.main()
