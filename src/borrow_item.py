from datetime import date, datetime

from src.device import Device


DateValue = date | datetime


class BorrowItem:
    """Thông tin mượn và trả của một thiết bị trong phiếu mượn."""

    def __init__(
        self,
        device: Device,
        borrowed_date: DateValue,
        from_period: int,
        to_period: int,
    ):
        if device is None:
            raise ValueError("Thiết bị không được để trống.")

        if not isinstance(borrowed_date, (date, datetime)):
            raise TypeError("Ngày mượn phải có kiểu date hoặc datetime.")

        if isinstance(from_period, bool) or not isinstance(from_period, int):
            raise TypeError("Tiết bắt đầu phải là số nguyên.")
        if isinstance(to_period, bool) or not isinstance(to_period, int):
            raise TypeError("Tiết kết thúc phải là số nguyên.")
        if from_period <= 0 or to_period <= 0:
            raise ValueError("Tiết mượn phải lớn hơn 0.")
        if to_period < from_period:
            raise ValueError("Tiết kết thúc phải lớn hơn hoặc bằng tiết bắt đầu.")

        self._device = device
        self._borrowed_date = borrowed_date
        self._from_period = from_period
        self._to_period = to_period
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
    def returned_date(self) -> DateValue | None:
        return self._returned_date

    @property
    def is_returned(self) -> bool:
        return self._returned_date is not None

    def return_device(self, returned_date: DateValue) -> None:
        """Ghi nhận ngày trả nếu thiết bị chưa được trả và ngày hợp lệ."""
        if self.is_returned:
            raise ValueError("Thiết bị trong mục mượn này đã được trả.")

        if not isinstance(returned_date, (date, datetime)):
            raise TypeError("Ngày trả phải có kiểu date hoặc datetime.")

        # So sánh ngày theo cùng kiểu để hỗ trợ cả date và datetime.
        borrowed_day = self._borrowed_date.date() if isinstance(self._borrowed_date, datetime) else self._borrowed_date
        returned_day = returned_date.date() if isinstance(returned_date, datetime) else returned_date
        if returned_day < borrowed_day:
            raise ValueError("Ngày trả không được trước ngày mượn.")

        self._returned_date = returned_date

    # Tên phương thức theo đề bài tiếng C#; giữ alias để dễ đối chiếu với đặc tả.
    def Return(self, returnedDate: DateValue) -> None:
        self.return_device(returnedDate)

    def __str__(self) -> str:
        return (
            f"Thiết bị: {self.device.device_id}, "
            f"Ngày mượn: {self.borrowed_date}, "
            f"Tiết: {self.from_period}-{self.to_period}, "
            f"Ngày trả: {self.returned_date if self.returned_date is not None else 'Chưa trả'}"
        )
