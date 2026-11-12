import unittest

from names import normalize_name


class NormalizeNameTests(unittest.TestCase):
    def test_empty_string_is_rejected(self):
        with self.assertRaisesRegex(ValueError, '^name required$'):
            normalize_name('')

    def test_whitespace_only_is_rejected(self):
        for name in ('  ', '\t\n', '\u3000'):
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError, '^name required$'):
                    normalize_name(name)

    def test_nonempty_names_are_trimmed_and_preserved(self):
        for name, expected in (
            ('  Alice  ', 'Alice'),
            (' 张三 ', '张三'),
            ('  Alice 张三  ', 'Alice 张三'),
            ('  aLiCe  ', 'aLiCe'),
        ):
            with self.subTest(name=name):
                self.assertEqual(normalize_name(name), expected)


if __name__ == '__main__':
    unittest.main()
