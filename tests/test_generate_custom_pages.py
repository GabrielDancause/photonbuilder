import unittest
import os
import sys

# Add root dir to path so we can import the script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generate_custom_pages import format_pct

class TestFormatPct(unittest.TestCase):
    def test_format_pct_positive_float(self):
        self.assertEqual(format_pct(12.345), "12.35%")
        self.assertEqual(format_pct(0.1), "0.10%")

    def test_format_pct_negative_float(self):
        self.assertEqual(format_pct(-5.678), "-5.68%")
        self.assertEqual(format_pct(-0.01), "-0.01%")

    def test_format_pct_zero(self):
        self.assertEqual(format_pct(0), "0.00%")
        self.assertEqual(format_pct(0.0), "0.00%")

    def test_format_pct_none(self):
        self.assertEqual(format_pct(None), "N/A")

    def test_format_pct_integer(self):
        self.assertEqual(format_pct(100), "100.00%")
        self.assertEqual(format_pct(-50), "-50.00%")

    def test_format_pct_large_number(self):
        self.assertEqual(format_pct(1234567.89), "1234567.89%")

if __name__ == '__main__':
    unittest.main()
