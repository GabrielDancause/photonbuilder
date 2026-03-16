import unittest
from generate_custom_pages import format_money

class TestGenerateCustomPages(unittest.TestCase):
    def test_format_money(self):
        # test None input
        self.assertEqual(format_money(None), "N/A")

        # test positive numeric inputs
        self.assertEqual(format_money(100), "$100.00")
        self.assertEqual(format_money(100.5), "$100.50")
        self.assertEqual(format_money(100.123), "$100.12")
        self.assertEqual(format_money(1000), "$1,000.00")
        self.assertEqual(format_money(1000000.12), "$1,000,000.12")

        # test zero
        self.assertEqual(format_money(0), "$0.00")
        self.assertEqual(format_money(0.0), "$0.00")

        # test negative inputs
        self.assertEqual(format_money(-100), "$-100.00")
        self.assertEqual(format_money(-100.5), "$-100.50")
        self.assertEqual(format_money(-1000), "$-1,000.00")

if __name__ == '__main__':
    unittest.main()
