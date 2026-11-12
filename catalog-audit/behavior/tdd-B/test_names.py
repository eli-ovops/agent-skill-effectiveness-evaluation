import unittest

from names import normalize_name


class NormalizeNameTests(unittest.TestCase):
    def test_empty_name_is_rejected(self):
        with self.assertRaises(ValueError) as raised:
            normalize_name('')
        self.assertEqual(str(raised.exception), 'name required')

    def test_whitespace_only_name_is_rejected(self):
        for name in (' ', '\t\n', '\u2003'):
            with self.subTest(name=name):
                with self.assertRaises(ValueError) as raised:
                    normalize_name(name)
                self.assertEqual(str(raised.exception), 'name required')

    def test_nonempty_name_is_trimmed_and_preserved(self):
        for name, expected in (('  Alice  ', 'Alice'), (' 张三 ', '张三'),
                               ('  aLiCe 张三  ', 'aLiCe 张三')):
            with self.subTest(name=name):
                self.assertEqual(normalize_name(name), expected)


if __name__ == '__main__':
    unittest.main()
