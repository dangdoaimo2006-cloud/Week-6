from datetime import date, datetime

from src.device import Device

DateValue = date | datetime


def _as_date(value: DateValue) -> date:
    return value.date() if isinstance(value, datetime) else value


class BorrowItem:
    """Thông tin mượn-trả của một thiết bị trong phiếu mượn."""

    def __init__(
        self,
        device: Device,
        borrowed_date: DateValue,
        from_period: int,
        to_period: int,
        due_date: DateValue | None = None,
    ):
        if device is None:
            raise ValueError("Thiết bị không được để trống.")
        if not isinstance(borrowed_date, (date, datetime)):
            raise TypeError("Ngày mượn phải có kiểu date hoặc datetime.")
        if isinstance(from_period, bool) or not isinstance(from_period, int):
            raise TypeError("Tiết bắt đầu phải là số nguyên.")
        if isinstance(to_period, bool) or not isinstance(to_period, int):
            raise TypeError("Tiết kết thúc phải là số nguyên.")
        if from_period <= 0 or to_period < from_period:
            raise ValueError("Khoảng tiết mượn không hợp lệ.")
        if due_date is None:
            due_date = borrowed_date
        if not isinstance(due_date, (date, datetime)):
            raise TypeError("Hạn trả phải có kiểu date hoặc datetime.")
        if _as_date(due_date) < _as_date(borrowed_date):
            raise ValueError("Hạn trả phải sau hoặc bằng ngày mượn.")

        self._device = device
        self._borrowed_date = borrowed_date
        self._from_period = from_period
        self._to_period = to_period
        self._due_date = due_date
        self._returned_date = None

    @property
    def device(self) -> Device:
        return self._device

    @property
    def borrowed_date(self) -> DateValue:
        return self._borrowed_date

    @property
    def from_period(self) -> int:
        return self._from_period

    @property
    def to_period(self) -> int:
        return self._to_period

    @property
    def due_date(self) -> DateValue:
        return self._due_date

    @property
    def returned_date(self) -> DateValue | None:
        return self._returned_date

    @property
    def is_returned(self) -> bool:
        return self._returned_date is not None

    def return_device(self, returned_date: DateValue) -> None:
        if self.is_returned:
            raise ValueError("Thiết bị trong mục mượn này đã được trả.")
        if not isinstance(returned_date, (date, datetime)):
            raise TypeError("Ngày trả phải có kiểu date hoặc datetime.")
        if _as_date(returned_date) < _as_date(self._borrowed_date):
            raise ValueError("Ngày trả không được trước ngày mượn.")
        self._returned_date = returned_date

    def Return(self, returnedDate: DateValue) -> None:
        """Tên phương thức tương ứng với chữ ký trong đề bài."""
        self.return_device(returnedDate)

    def __str__(self) -> str:
        returned = self.returned_date if self.is_returned else "Chưa trả"
        return (
            f"Thiết bị: {self.device.device_id}, Ngày mượn: {self.borrowed_date}, "
            f"Hạn trả: {self.due_date}, Tiết: {self.from_period}-{self.to_period}, "
            f"Ngày trả: {returned}"
        )
