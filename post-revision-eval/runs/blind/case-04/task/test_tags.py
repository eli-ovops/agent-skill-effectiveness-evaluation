import unittest

from tags import normalize_tag


class NormalizeTagTest(unittest.TestCase):
    def test_normalizes_tags_and_rejects_empty_values(self):
        for value, expected in (
            ("  Blue  ", "Blue"),
            (" 茶 ", "茶"),
            (" MiXeD 标签 ", "MiXeD 标签"),
        ):
            with self.subTest(value=value):
                self.assertEqual(normalize_tag(value), expected)

        for value in ("", "   ", "\t\n"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError) as error:
                    normalize_tag(value)
                self.assertEqual(str(error.exception), "tag required")


if __name__ == "__main__":
    unittest.main()
