import unittest

from summary import format_summary, summarize


class SummaryTests(unittest.TestCase):
    def test_groups_trim_names_preserve_case_and_include_zero(self):
        result = summarize([
            {'group': ' 红 ', 'units': 2},
            {'group': '红', 'units': 0},
            {'group': '蓝', 'units': 3},
            {'group': 'A', 'units': 0},
            {'group': 'a', 'units': 1},
        ])
        self.assertEqual(result, {
            'records': 5,
            'total': 6,
            'groups': {'A': 0, 'a': 1, '红': 2, '蓝': 3},
        })
        self.assertEqual(list(result['groups']), ['A', 'a', '红', '蓝'])

    def test_empty_list(self):
        result = summarize([])
        self.assertEqual(result, {'records': 0, 'total': 0, 'groups': {}})
        self.assertEqual(format_summary(result), 'Records: 0\nTotal units: 0')

    def test_invalid_records_raise_value_error(self):
        invalid = [
            None, {}, {'units': 1}, {'group': 'A'},
            {'group': '' , 'units': 1}, {'group': ' \t ', 'units': 1},
            {'group': 1, 'units': 1}, {'group': 'A', 'units': -1},
            {'group': 'A', 'units': True}, {'group': 'A', 'units': False},
            {'group': 'A', 'units': 1.0}, {'group': 'A', 'units': '1'},
        ]
        for record in invalid:
            with self.subTest(record=record):
                with self.assertRaisesRegex(ValueError, '^invalid record$'):
                    summarize([record])

    def test_format_sorts_groups_even_when_input_is_unsorted(self):
        summary = {'records': 3, 'total': 5, 'groups': {'蓝': 3, '红': 2}}
        self.assertEqual(
            format_summary(summary),
            'Records: 3\nTotal units: 5\n红: 2\n蓝: 3',
        )


if __name__ == '__main__':
    unittest.main()
