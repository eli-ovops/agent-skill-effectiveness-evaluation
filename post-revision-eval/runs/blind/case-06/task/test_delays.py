import unittest

from delays import export_status, render_status


CASES = (
    ('default within limit', (5,), False),
    ('default at limit', (30,), False),
    ('default above limit', (31,), True),
    ('zero limit', (5, 0), True),
    ('zero at limit', (0, 0), False),
    ('explicit limit', (5, 8), False),
    ('explicit at limit', (8, 8), False),
)


class StatusTests(unittest.TestCase):
    def test_render_status(self):
        for name, args, late in CASES:
            with self.subTest(name=name):
                self.assertEqual(render_status(*args), 'late' if late else 'ok')

    def test_export_status(self):
        for name, args, late in CASES:
            with self.subTest(name=name):
                self.assertEqual(export_status(*args), {'late': late})


if __name__ == '__main__':
    unittest.main()
