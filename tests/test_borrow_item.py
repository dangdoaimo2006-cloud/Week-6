import unittest
from datetime import date, datetime, timedelta

from src.borrow_item import BorrowItem
from src.device import Microphone


class TestBorrowItem(unittest.TestCase):
    def setUp(self):
        self.device = Microphone("MIC01", "Micro khong day", 2023, 1_000_000)
        self.borrowed_date = date(2026, 10, 17)

    def test_create_borrow_item(self):
        item = BorrowItem(self.device, self.borrowed_date, 1, 2)

        self.assertIs(item.device, self.device)
        self.assertEqual(item.borrowed_date, self.borrowed_date)
        self.assertEqual(item.from_period, 1)
        self.assertEqual(item.to_period, 2)
        self.assertIsNone(item.returned_date)
        self.assertFalse(item.is_returned)

    def test_device_cannot_be_none(self):
        with self.assertRaises(ValueError):
            BorrowItem(None, self.borrowed_date, 1, 1)

    def test_periods_must_be_positive(self):
        with self.assertRaises(ValueError):
            BorrowItem(self.device, self.borrowed_date, 0, 1)

    def test_end_period_cannot_precede_start_period(self):
        with self.assertRaises(ValueError):
            BorrowItem(self.device, self.borrowed_date, 3, 2)

    def test_period_must_be_integer(self):
        with self.assertRaises(TypeError):
            BorrowItem(self.device, self.borrowed_date, 1.5, 2)

    def test_return_device(self):
        item = BorrowItem(self.device, self.borrowed_date, 1, 2)
        return_date = self.borrowed_date + timedelta(days=1)

        item.return_device(return_date)

        self.assertEqual(item.returned_date, return_date)
        self.assertTrue(item.is_returned)

    def test_return_date_cannot_precede_borrow_date(self):
        item = BorrowItem(self.device, self.borrowed_date, 1, 1)

        with self.assertRaises(ValueError):
            item.return_device(self.borrowed_date - timedelta(days=1))

        self.assertFalse(item.is_returned)
        self.assertIsNone(item.returned_date)

    def test_item_cannot_be_returned_twice(self):
        item = BorrowItem(self.device, self.borrowed_date, 1, 1)
        item.return_device(self.borrowed_date)

        with self.assertRaises(ValueError):
            item.return_device(self.borrowed_date + timedelta(days=1))

    def test_accepts_datetime(self):
        borrowed = datetime(2026, 10, 17, 8, 0)
        item = BorrowItem(self.device, borrowed, 1, 1)
        returned = datetime(2026, 10, 17, 10, 0)

        item.return_device(returned)

        self.assertEqual(item.returned_date, returned)

    def test_string_representation(self):
        item = BorrowItem(self.device, self.borrowed_date, 1, 2)

        self.assertIn("MIC01", str(item))
        self.assertIn("Chua tra", str(item))


if __name__ == "__main__":
    unittest.main()
