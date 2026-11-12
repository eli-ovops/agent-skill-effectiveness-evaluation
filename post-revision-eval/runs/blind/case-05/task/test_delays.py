import unittest

from delays import export_status, render_status


class StatusTests(unittest.TestCase):
    def test_text_and_export_entry_points(self):
        cases = (
            ('default at limit', (30,), 'ok', {'late': False}),
            ('default above limit', (31,), 'late', {'late': True}),
            ('explicit zero', (5, 0), 'late', {'late': True}),
            ('below explicit limit', (5, 8), 'ok', {'late': False}),
            ('equal to explicit limit', (8, 8), 'ok', {'late': False}),
            ('zero equals zero limit', (0, 0), 'ok', {'late': False}),
        )
        for name, args, text, exported in cases:
            with self.subTest(case=name, entry='text'):
                self.assertEqual(render_status(*args), text)
            with self.subTest(case=name, entry='export'):
                self.assertEqual(export_status(*args), exported)


if __name__ == '__main__':
    unittest.main()
