import unittest

from tags import normalize_tag


class NormalizeTagTests(unittest.TestCase):
    def test_trims_nonempty_tags_without_changing_content(self):
        cases = (
            ("  Blue  ", "Blue"),
            (" 茶 ", "茶"),
            (" \tMiXeD 中文 标签 \n ", "MiXeD 中文 标签"),
        )
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(normalize_tag(value), expected)

    def test_rejects_empty_and_whitespace_only_tags(self):
        for value in ("", " \t\n "):
            with self.subTest(value=value):
                with self.assertRaises(ValueError) as error:
                    normalize_tag(value)
                self.assertEqual(str(error.exception), "tag required")


if __name__ == "__main__":
    unittest.main()
