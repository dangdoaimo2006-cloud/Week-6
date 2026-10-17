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


# Moi phieu muon gan voi mot nguoi muon va quan ly danh sach thiet bi rieng.
class BorrowingSlip:
    """Phieu muon; so huu cac BorrowItem nhung chi tham chieu đen Device."""

    # Đe bai chua chi đinh muc phi tra muon; đay la gia đinh co the cau hinh.
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
            raise ValueError("Ma phieu muon khong đuoc đe trong.")
        if borrower is None or not isinstance(borrower, IBorrower):
            raise ValueError("Nguoi muon khong hop le.")
        if not isinstance(teaching_room, str) or not teaching_room.strip():
            raise ValueError("Phong giang day khong đuoc đe trong.")
        if borrowed_date is None:
            borrowed_date = date.today()
        if not isinstance(borrowed_date, (date, datetime)):
            raise TypeError("Ngay muon phai co kieu date hoac datetime.")
        if late_fee_per_day is not None and late_fee_per_day < 0:
            raise ValueError("Phi tra muon moi ngay khong đuoc am.")

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
        # Tra ve ban bat bien đe ben ngoai khong sua truc tiep danh sach noi bo.
        return tuple(self._items)

    def add_device(self, device: Device, borrow_days: int) -> None:
        """Kiem tra toan bo đieu kien truoc khi đoi trang thai hoac them item."""
        if device is None:
            raise ValueError("Thiet bi khong đuoc đe trong.")
        if isinstance(borrow_days, bool) or not isinstance(borrow_days, int):
            raise TypeError("So ngay muon phai la so nguyen.")
        if borrow_days <= 0:
            raise InvalidBorrowPeriodException(
                device.device_id, borrow_days, getattr(device, "max_borrow_days", 1)
            )
        # Moi thiet bi chi duoc xuat hien mot lan trong cung mot phieu muon.
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

        # Su dung so ngay theo lich vi de bai chua quy dinh cach tinh khac.
        due_date = self._borrowed_date + timedelta(days=borrow_days)
        item = BorrowItem(
            device=device,
            borrowed_date=self._borrowed_date,
            from_period=1,
            to_period=1,
            due_date=due_date,
        )
        # Chi cap nhat trang thai sau khi moi kiem tra va viec tao item thanh cong.
        device.status = DeviceStatus.BORROWED
        self._items.append(item)

    def return_device(self, device_id: str, returned_date: DateValue) -> float:
        if not isinstance(device_id, str) or not device_id.strip():
            raise ValueError("Ma thiet bi khong đuoc đe trong.")
        item = next(
            (entry for entry in self._items if entry.device.device_id == device_id),
            None,
        )
        if item is None:
            raise DeviceNotInSlipException(device_id)
        if item.is_returned:
            raise DeviceAlreadyReturnedException(device_id)
        if not isinstance(returned_date, (date, datetime)):
            raise TypeError("Ngay tra phai co kieu date hoac datetime.")
        if _as_date(returned_date) < _as_date(item.borrowed_date):
            raise InvalidReturnDateException(device_id, returned_date, item.borrowed_date)

        # Tinh phi truoc; sau khi xac thuc xong moi cap nhat trang thai hai đoi tuong.
        late_days = max(0, (_as_date(returned_date) - _as_date(item.due_date)).days)
        # Khong tinh phi neu tra som hoac dung han.
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
                # Voi thiet bi chua tra, tinh phi tam tinh đen ngay hien tai.
                late_days = max(0, (date.today() - _as_date(item.due_date)).days)
            total += late_days * self._late_fee_per_day
        return total

    def get_late_or_unreturned_items(self) -> tuple[BorrowItem, ...]:
        """Tra ve cac muc đa qua han hoac chua đuoc tra."""
        today = date.today()
        return tuple(
            item
            for item in self._items
            if not item.is_returned or _as_date(item.returned_date) > _as_date(item.due_date)
            or (not item.is_returned and today > _as_date(item.due_date))
        )

    # Cac alias theo ten phuong thuc trong đac ta C#.
    def AddDevice(self, device: Device, borrowDays: int) -> None:
        self.add_device(device, borrowDays)

    def ReturnDevice(self, deviceId: str, returnedDate: DateValue) -> float:
        return self.return_device(deviceId, returnedDate)

    def CalculateTotalLateFee(self) -> float:
        return self.calculate_total_late_fee()

    def __str__(self) -> str:
        return (
            f"Phieu: {self.slip_id}, Nguoi muon: {self.borrower.full_name}, "
            f"Phong: {self.teaching_room}, Ngay muon: {self.borrowed_date}, "
            f"So thiet bi: {len(self.items)}"
        )
