from datetime import date, datetime

from src.device import Device

DateValue = date | datetime


# Chi so sanh ngay, khong can so sanh ca gio khi tinh phi tre han.
def _as_date(value: DateValue) -> date:
    return value.date() if isinstance(value, datetime) else value


class BorrowItem:
    """Thong tin muon-tra cua mot thiet bi trong phieu muon."""

    def __init__(
        self,
        device: Device,
        borrowed_date: DateValue,
        from_period: int,
        to_period: int,
        due_date: DateValue | None = None,
    ):
        if device is None:
            raise ValueError("Thiet bi khong đuoc đe trong.")
        if not isinstance(borrowed_date, (date, datetime)):
            raise TypeError("Ngay muon phai co kieu date hoac datetime.")
        if isinstance(from_period, bool) or not isinstance(from_period, int):
            raise TypeError("Tiet bat đau phai la so nguyen.")
        if isinstance(to_period, bool) or not isinstance(to_period, int):
            raise TypeError("Tiet ket thuc phai la so nguyen.")
        if from_period <= 0 or to_period < from_period:
            raise ValueError("Khoang tiet muon khong hop le.")
        if due_date is None:
            due_date = borrowed_date
        if not isinstance(due_date, (date, datetime)):
            raise TypeError("Han tra phai co kieu date hoac datetime.")
        if _as_date(due_date) < _as_date(borrowed_date):
            raise ValueError("Han tra phai sau hoac bang ngay muon.")

        self._device = device
        self._borrowed_date = borrowed_date
        self._from_period = from_period
        self._to_period = to_period
        self._due_date = due_date
        # Gia tri None nghia la thiet bi van chua duoc tra.
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
            raise ValueError("Thiet bi trong muc muon nay đa đuoc tra.")
        if not isinstance(returned_date, (date, datetime)):
            raise TypeError("Ngay tra phai co kieu date hoac datetime.")
        if _as_date(returned_date) < _as_date(self._borrowed_date):
            raise ValueError("Ngay tra khong đuoc truoc ngay muon.")
        # Chi luu ngay tra sau khi cac dieu kien hop le.
        self._returned_date = returned_date

    def Return(self, returnedDate: DateValue) -> None:
        """Ten phuong thuc tuong ung voi chu ky trong đe bai."""
        self.return_device(returnedDate)

    def __str__(self) -> str:
        returned = self.returned_date if self.is_returned else "Chua tra"
        return (
            f"Thiet bi: {self.device.device_id}, Ngay muon: {self.borrowed_date}, "
            f"Han tra: {self.due_date}, Tiet: {self.from_period}-{self.to_period}, "
            f"Ngay tra: {returned}"
        )
