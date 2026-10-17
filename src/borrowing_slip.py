from datetime import date, datetime, timedelta
from typing import Iterable

from src.borrow_item import BorrowItem, DateValue
from src.borrower import IBorrower
from src.device import Device, DeviceStatus
from src.exceptions import (
    BorrowLimitExceededException,
    DeviceAlreadyReturnedException,
    DeviceNotInSlipException,
    DeviceUnavailableException,
    DuplicateDeviceException,
    InvalidBorrowPeriodException,
    InvalidReturnDateException,
)


def _as_date(value: DateValue) -> date:
    return value.date() if isinstance(value, datetime) else value


class BorrowingSlip:
    """Phiếu mượn; sở hữu các BorrowItem nhưng chỉ tham chiếu đến Device."""

    # Đề bài chưa chỉ định mức phí trả muộn; đây là giả định có thể cấu hình.
    LATE_FEE_PER_DAY = 10_000

    def __init__(
        self,
        slip_id: str,
        borrower: IBorrower,
        teaching_room: str,
        borrowed_date: DateValue | None = None,
        late_fee_per_day: float | None = None,
    ):
        if not isinstance(slip_id, str) or not slip_id.strip():
            raise ValueError("Mã phiếu mượn không được để trống.")
        if borrower is None or not isinstance(borrower, IBorrower):
            raise ValueError("Người mượn không hợp lệ.")
        if not isinstance(teaching_room, str) or not teaching_room.strip():
            raise ValueError("Phòng giảng dạy không được để trống.")
        if borrowed_date is None:
            borrowed_date = date.today()
        if not isinstance(borrowed_date, (date, datetime)):
            raise TypeError("Ngày mượn phải có kiểu date hoặc datetime.")
        if late_fee_per_day is not None and late_fee_per_day < 0:
            raise ValueError("Phí trả muộn mỗi ngày không được âm.")

        self._slip_id = slip_id.strip()
        self._borrower = borrower
        self._teaching_room = teaching_room.strip()
        self._borrowed_date = borrowed_date
        self._items: list[BorrowItem] = []
        self._late_fee_per_day = (
            self.LATE_FEE_PER_DAY if late_fee_per_day is None else late_fee_per_day
        )

    @property
    def slip_id(self) -> str:
        return self._slip_id

    @property
    def borrower(self) -> IBorrower:
        return self._borrower

    @property
    def teaching_room(self) -> str:
        return self._teaching_room

    @property
    def borrowed_date(self) -> DateValue:
        return self._borrowed_date

    @property
    def items(self) -> tuple[BorrowItem, ...]:
        # Trả về bản bất biến để bên ngoài không sửa trực tiếp danh sách nội bộ.
        return tuple(self._items)

    def add_device(self, device: Device, borrow_days: int) -> None:
        """Kiểm tra toàn bộ điều kiện trước khi đổi trạng thái hoặc thêm item."""
        if device is None:
            raise ValueError("Thiết bị không được để trống.")
        if isinstance(borrow_days, bool) or not isinstance(borrow_days, int):
            raise TypeError("Số ngày mượn phải là số nguyên.")
        if borrow_days <= 0:
            raise InvalidBorrowPeriodException(
                device.device_id, borrow_days, getattr(device, "max_borrow_days", 1)
            )
        if any(item.device.device_id == device.device_id for item in self._items):
            raise DuplicateDeviceException(device.device_id)
        if len(self._items) >= self._borrower.get_maximum_devices():
            raise BorrowLimitExceededException(
                self._borrower.borrower_id, self._borrower.get_maximum_devices()
            )
        if device.status != DeviceStatus.AVAILABLE:
            raise DeviceUnavailableException(device.device_id, device.status)

        maximum_days = getattr(device, "max_borrow_days", 1)
        if borrow_days > maximum_days:
            raise InvalidBorrowPeriodException(device.device_id, borrow_days, maximum_days)

        due_date = self._borrowed_date + timedelta(days=borrow_days)
        item = BorrowItem(
            device=device,
            borrowed_date=self._borrowed_date,
            from_period=1,
            to_period=1,
            due_date=due_date,
        )
        # Chỉ cập nhật trạng thái sau khi mọi kiểm tra và việc tạo item thành công.
        device.status = DeviceStatus.BORROWED
        self._items.append(item)

    def return_device(self, device_id: str, returned_date: DateValue) -> float:
        if not isinstance(device_id, str) or not device_id.strip():
            raise ValueError("Mã thiết bị không được để trống.")
        item = next(
            (entry for entry in self._items if entry.device.device_id == device_id),
            None,
        )
        if item is None:
            raise DeviceNotInSlipException(device_id)
        if item.is_returned:
            raise DeviceAlreadyReturnedException(device_id)
        if not isinstance(returned_date, (date, datetime)):
            raise TypeError("Ngày trả phải có kiểu date hoặc datetime.")
        if _as_date(returned_date) < _as_date(item.borrowed_date):
            raise InvalidReturnDateException(device_id, returned_date, item.borrowed_date)

        # Tính phí trước; sau khi xác thực xong mới cập nhật trạng thái hai đối tượng.
        late_days = max(0, (_as_date(returned_date) - _as_date(item.due_date)).days)
        late_fee = late_days * self._late_fee_per_day
        item.return_device(returned_date)
        item.device.status = DeviceStatus.AVAILABLE
        return late_fee

    def calculate_total_late_fee(self) -> float:
        total = 0.0
        for item in self._items:
            if item.is_returned:
                late_days = max(
                    0,
                    (_as_date(item.returned_date) - _as_date(item.due_date)).days,
                )
            else:
                # Với thiết bị chưa trả, tính phí tạm tính đến ngày hiện tại.
                late_days = max(0, (date.today() - _as_date(item.due_date)).days)
            total += late_days * self._late_fee_per_day
        return total

    def get_late_or_unreturned_items(self) -> tuple[BorrowItem, ...]:
        """Trả về các mục đã quá hạn hoặc chưa được trả."""
        today = date.today()
        return tuple(
            item
            for item in self._items
            if not item.is_returned or _as_date(item.returned_date) > _as_date(item.due_date)
            or (not item.is_returned and today > _as_date(item.due_date))
        )

    # Các alias theo tên phương thức trong đặc tả C#.
    def AddDevice(self, device: Device, borrowDays: int) -> None:
        self.add_device(device, borrowDays)

    def ReturnDevice(self, deviceId: str, returnedDate: DateValue) -> float:
        return self.return_device(deviceId, returnedDate)

    def CalculateTotalLateFee(self) -> float:
        return self.calculate_total_late_fee()

    def __str__(self) -> str:
        return (
            f"Phiếu: {self.slip_id}, Người mượn: {self.borrower.full_name}, "
            f"Phòng: {self.teaching_room}, Ngày mượn: {self.borrowed_date}, "
            f"Số thiết bị: {len(self.items)}"
        )
