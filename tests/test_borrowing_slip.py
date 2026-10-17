import unittest
from datetime import date, timedelta

from src.borrower import Lecturer, TeachingAssistant
from src.borrowing_slip import BorrowingSlip
from src.device import DeviceStatus, Microphone, ProjectorRemote, AirConditionerRemote
from src.exceptions import (
    BorrowLimitExceededException,
    DeviceAlreadyReturnedException,
    DeviceNotInSlipException,
    DeviceUnavailableException,
    DuplicateDeviceException,
    InvalidBorrowPeriodException,
    InvalidReturnDateException,
)


class TestBorrowingSlip(unittest.TestCase):
    def setUp(self):
        self.borrowed_date = date(2026, 10, 1)
        self.lecturer = Lecturer("GV01", "Nguyen Van A")
        self.slip = BorrowingSlip("PM01", self.lecturer, "P101", self.borrowed_date)

    def test_successful_borrow_and_return_on_time(self):
        device = ProjectorRemote("PR01", "Dieu khien may chieu", 2022, 400_000)
        self.slip.add_device(device, 1)

        self.assertEqual(device.status, DeviceStatus.BORROWED)
        self.assertEqual(len(self.slip.items), 1)
        fee = self.slip.return_device("PR01", self.borrowed_date + timedelta(days=1))

        self.assertEqual(fee, 0)
        self.assertEqual(device.status, DeviceStatus.AVAILABLE)
        self.assertTrue(self.slip.items[0].is_returned)

    def test_late_return_fee_for_two_days(self):
        device = Microphone("MIC01", "Micro", 2023, 1_000_000, max_borrow_days=1)
        self.slip.add_device(device, 1)
        fee = self.slip.return_device("MIC01", self.borrowed_date + timedelta(days=3))
        self.assertEqual(fee, 20_000)
        self.assertEqual(self.slip.calculate_total_late_fee(), 20_000)

    def test_unavailable_device_does_not_change_slip(self):
        device = AirConditionerRemote(
            "AC01", "Remote dieu hoa", 2020, 200_000,
            status=DeviceStatus.UNDER_MAINTENANCE,
        )
        with self.assertRaises(DeviceUnavailableException):
            self.slip.add_device(device, 1)
        self.assertEqual(device.status, DeviceStatus.UNDER_MAINTENANCE)
        self.assertEqual(len(self.slip.items), 0)

    def test_borrower_limit_exceeded(self):
        assistant = TeachingAssistant("TA01", "Tran Thi B")
        slip = BorrowingSlip("PM02", assistant, "P102", self.borrowed_date)
        devices = [
            Microphone("M1", "Micro 1", 2023, 100_000),
            Microphone("M2", "Micro 2", 2023, 100_000),
            Microphone("M3", "Micro 3", 2023, 100_000),
        ]
        slip.add_device(devices[0], 1)
        slip.add_device(devices[1], 1)
        with self.assertRaises(BorrowLimitExceededException):
            slip.add_device(devices[2], 1)
        self.assertEqual(len(slip.items), 2)
        self.assertEqual(devices[2].status, DeviceStatus.AVAILABLE)

    def test_duplicate_device(self):
        device = Microphone("MIC01", "Micro", 2023, 1_000_000)
        self.slip.add_device(device, 1)
        with self.assertRaises(DuplicateDeviceException):
            self.slip.add_device(device, 1)
        self.assertEqual(len(self.slip.items), 1)

    def test_borrow_period_exceeds_device_limit(self):
        device = Microphone("MIC01", "Micro", 2023, 1_000_000, max_borrow_days=1)
        with self.assertRaises(InvalidBorrowPeriodException):
            self.slip.add_device(device, 3)
        self.assertEqual(device.status, DeviceStatus.AVAILABLE)
        self.assertEqual(len(self.slip.items), 0)

    def test_return_device_not_in_slip(self):
        with self.assertRaises(DeviceNotInSlipException):
            self.slip.return_device("UNKNOWN", self.borrowed_date)

    def test_return_device_twice(self):
        device = Microphone("MIC01", "Micro", 2023, 1_000_000)
        self.slip.add_device(device, 1)
        return_date = self.borrowed_date + timedelta(days=1)
        self.slip.return_device("MIC01", return_date)
        with self.assertRaises(DeviceAlreadyReturnedException):
            self.slip.return_device("MIC01", return_date)

    def test_return_date_before_borrow_date(self):
        device = Microphone("MIC01", "Micro", 2023, 1_000_000)
        self.slip.add_device(device, 1)
        with self.assertRaises(InvalidReturnDateException):
            self.slip.return_device("MIC01", self.borrowed_date - timedelta(days=1))
        self.assertFalse(self.slip.items[0].is_returned)
        self.assertEqual(device.status, DeviceStatus.BORROWED)

    def test_invalid_slip_id(self):
        with self.assertRaises(ValueError):
            BorrowingSlip("  ", self.lecturer, "P101", self.borrowed_date)


if __name__ == "__main__":
    unittest.main()
