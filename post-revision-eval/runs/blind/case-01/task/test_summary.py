import unittest
from collections import UserDict

from summary import format_summary, summarize


class SummaryTests(unittest.TestCase):
    def test_merge_trim_case_sort_and_format(self):
        result = summarize([
            {'group': ' z ', 'units': 2},
            {'group': 'A', 'units': 3},
            {'group': 'z', 'units': 0},
            {'group': 'a', 'units': 4},
        ])
        self.assertEqual(result, {
            'records': 4, 'total': 9, 'groups': {'A': 3, 'a': 4, 'z': 2}
        })
        self.assertEqual(list(result['groups']), ['A', 'a', 'z'])
        result['groups'] = {'z': 2, 'a': 4, 'A': 3}
        self.assertEqual(format_summary(result),
                         'Records: 4\nTotal units: 9\nA: 3\na: 4\nz: 2')
        self.assertEqual(summarize([UserDict(group='B', units=1)]),
                         {'records': 1, 'total': 1, 'groups': {'B': 1}})

    def test_empty(self):
        result = summarize([])
        self.assertEqual(result, {'records': 0, 'total': 0, 'groups': {}})
        self.assertEqual(format_summary(result), 'Records: 0\nTotal units: 0')

    def test_invalid_records(self):
        invalid = [None, {}, {'group': 'a'}, {'units': 1},
                   {'group': None, 'units': 1}, {'group': ' \t', 'units': 1},
                   {'group': 'a', 'units': -1}, {'group': 'a', 'units': 1.0},
                   {'group': 'a', 'units': True}, {'group': 'a', 'units': False}]
        for record in invalid:
            with self.subTest(record=record):
                with self.assertRaisesRegex(ValueError, '^invalid record$'):
                    summarize([record])


if __name__ == '__main__':
    unittest.main()
