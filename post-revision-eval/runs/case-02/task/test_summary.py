import unittest

from summary import format_summary, summarize


class SummaryTests(unittest.TestCase):
    def test_combines_trimmed_groups_and_preserves_case(self):
        records = [
            {'group': ' Blue ', 'units': 3},
            {'group': 'Red', 'units': 2},
            {'group': '\tRed\n', 'units': 0},
            {'group': 'red', 'units': 4},
        ]
        result = summarize(records)
        self.assertEqual(result, {
            'records': 4,
            'total': 9,
            'groups': {'Blue': 3, 'Red': 2, 'red': 4},
        })
        self.assertEqual(list(result['groups']), ['Blue', 'Red', 'red'])

    def test_empty_input_and_formatted_output(self):
        self.assertEqual(summarize([]), {'records': 0, 'total': 0, 'groups': {}})
        self.assertEqual(format_summary(summarize([])), 'Records: 0\nTotal units: 0')

    def test_format_sorts_groups_without_trailing_newline(self):
        summary = {'records': 3, 'total': 5, 'groups': {'红': 2, '蓝': 3}}
        self.assertEqual(format_summary(summary),
                         'Records: 3\nTotal units: 5\n红: 2\n蓝: 3')

    def test_invalid_records(self):
        invalid_records = [
            {}, {'group': 'A'}, {'units': 1}, None, [],
            {'group': None, 'units': 1}, {'group': ' \t\n', 'units': 1},
            {'group': 'A', 'units': -1}, {'group': 'A', 'units': 1.5},
            {'group': 'A', 'units': '1'}, {'group': 'A', 'units': True},
            {'group': 'A', 'units': False},
        ]
        for record in invalid_records:
            with self.subTest(record=record):
                with self.assertRaisesRegex(ValueError, '^invalid record$'):
                    summarize([record])


if __name__ == '__main__':
    unittest.main()
