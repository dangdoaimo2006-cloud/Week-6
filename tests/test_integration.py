"""Kiểm thử tích hợp luồng phòng học - phiếu mượn - thiết bị."""
import unittest
from datetime import date

from src.borrower import Lecturer, TeachingAssistant
from src.borrowing_slip import BorrowingSlip
from src.class_room import ClassRoom
from src.device import DeviceStatus, Microphone, ProjectorRemote
from src.exceptions import BorrowLimitExceededException, DeviceUnavailableException


class TestBorrowingWorkflow(unittest.TestCase):
    def setUp(self):
        self.room = ClassRoom("P101", "Phòng học 101", 40)
        self.mic = Microphone(
            "MIC01", "Micro không dây", 2023, 1_000_000, max_borrow_days=3
        )
        self.remote = ProjectorRemote(
            "PRJ01", "Điều khiển máy chiếu", 2022, 500_000, max_borrow_days=2
        )
        self.room.add_device(self.mic)
        self.room.add_device(self.remote)

    def test_complete_borrow_return_workflow(self):
        borrower = Lecturer("GV01", "Nguyễn Văn An")
        slip = BorrowingSlip("PM01", borrower, self.room.room_id, date(2026, 10, 1), 10_000)

        slip.add_device(self.mic, 2)
        self.assertEqual(self.mic.status, DeviceStatus.BORROWED)
        self.assertIs(self.room.find_device("MIC01"), self.mic)

        fee = slip.return_device("MIC01", date(2026, 10, 5))
        self.assertEqual(fee, 20_000)
        self.assertEqual(self.mic.status, DeviceStatus.AVAILABLE)
        self.assertEqual(slip.calculate_total_late_fee(), 20_000)

    def test_failure_does_not_change_device_or_slip(self):
        borrower = TeachingAssistant("TA01", "Trợ giảng Bình")
        slip = BorrowingSlip("PM02", borrower, self.room.room_id, date(2026, 10, 1))
        self.mic.status = DeviceStatus.UNDER_MAINTENANCE

        with self.assertRaises(DeviceUnavailableException):
            slip.add_device(self.mic, 1)

        self.assertEqual(self.mic.status, DeviceStatus.UNDER_MAINTENANCE)
        self.assertEqual(len(slip.items), 0)

    def test_borrower_limit_is_enforced_across_slip_items(self):
        borrower = TeachingAssistant("TA02", "Trợ giảng Chi")
        slip = BorrowingSlip("PM03", borrower, self.room.room_id, date(2026, 10, 1))
        third = Microphone("MIC02", "Micro dự phòng", 2024, 800_000)
        self.room.add_device(third)
        slip.add_device(self.mic, 1)
        slip.add_device(self.remote, 1)

        with self.assertRaises(BorrowLimitExceededException):
            slip.add_device(third, 1)

        self.assertEqual(len(slip.items), 2)
        self.assertEqual(third.status, DeviceStatus.AVAILABLE)


if __name__ == "__main__":
    unittest.main()
