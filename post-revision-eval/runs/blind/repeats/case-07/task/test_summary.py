import unittest

from summary import format_summary, summarize


class SummaryTests(unittest.TestCase):
    def test_aggregates_trimmed_groups_preserving_case(self):
        result = summarize([
            {"group": " red ", "units": 2},
            {"group": "red", "units": 0},
            {"group": "Blue", "units": 3},
            {"group": "Red", "units": 4},
        ])
        self.assertEqual(result, {
            "records": 4,
            "total": 9,
            "groups": {"Blue": 3, "Red": 4, "red": 2},
        })
        self.assertEqual(list(result["groups"]), ["Blue", "Red", "red"])

    def test_empty_records(self):
        result = summarize([])
        self.assertEqual(result, {"records": 0, "total": 0, "groups": {}})
        self.assertEqual(format_summary(result), "Records: 0\nTotal units: 0")

    def test_rejects_invalid_records(self):
        invalid_records = [
            {},
            {"group": "A"},
            {"units": 1},
            {"group": " \t ", "units": 1},
            {"group": 1, "units": 1},
            {"group": "A", "units": -1},
            {"group": "A", "units": 1.0},
            {"group": "A", "units": True},
            {"group": "A", "units": False},
            None,
        ]
        for record in invalid_records:
            with self.subTest(record=record):
                with self.assertRaisesRegex(ValueError, r"^invalid record$"):
                    summarize([record])

    def test_formats_groups_in_order_without_trailing_newline(self):
        summary = {"records": 3, "total": 5, "groups": {"red": 2, "blue": 3}}
        self.assertEqual(
            format_summary(summary),
            "Records: 3\nTotal units: 5\nblue: 3\nred: 2",
        )


if __name__ == "__main__":
    unittest.main()
