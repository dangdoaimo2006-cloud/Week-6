from abc import ABC, abstractmethod
from datetime import date
from enum import Enum


# Cac loai thiet bi deu su dung chung cac trang thai nay.
class DeviceStatus(Enum):
    AVAILABLE = "Available"
    BORROWED = "Borrowed"
    UNDER_MAINTENANCE = "UnderMaintenance"


class Device(ABC):
    def __init__(
        self,
        device_id: str,
        name: str,
        year_introduced: int,
        purchase_price: float,
        status: DeviceStatus = DeviceStatus.AVAILABLE,
        max_borrow_days: int = 1,
    ):
        if not device_id or not device_id.strip():
            raise ValueError("Ma thiet bi khong đuoc đe trong.")

        if not name or not name.strip():
            raise ValueError("Ten thiet bi khong đuoc đe trong.")

        if purchase_price <= 0:
            raise ValueError("Gia mua phai lon hon 0.")

        if year_introduced > date.today().year:
            raise ValueError(
                "Nam đua vao su dung khong đuoc lon hon nam hien tai."
            )

        if not isinstance(status, DeviceStatus):
            raise TypeError("Trang thai thiet bi khong hop le.")

        if isinstance(max_borrow_days, bool) or not isinstance(max_borrow_days, int):
            raise TypeError("Thoi han muon toi đa phai la so nguyen.")
        if max_borrow_days <= 0:
            raise ValueError("Thoi han muon toi đa phai lon hon 0.")

        # Giu ma thiet bi o dang rieng; ben ngoai chi nen doc, khong nen thay doi.
        self._device_id = device_id.strip()
        self.name = name.strip()
        self.year_introduced = year_introduced
        self.purchase_price = float(purchase_price)
        self.status = status
        self.max_borrow_days = max_borrow_days

    @property
    def device_id(self):
        return self._device_id

    @abstractmethod
    def calculate_annual_maintenance_cost(self) -> float:
        pass

    def __str__(self):
        return (
            f"Ma: {self.device_id}, "
            f"Ten: {self.name}, "
            f"Nam su dung: {self.year_introduced}, "
            f"Gia mua: {self.purchase_price:.2f}, "
            f"Trang thai: {self.status.value}, "
            f"Thoi han muon toi đa: {self.max_borrow_days} ngay"
        )


# De bai chua dua ra cong thuc, nen tam su dung gia dinh bang 5% gia mua.
class AirConditionerRemote(Device):
    def calculate_annual_maintenance_cost(self) -> float:
        # Tam dung 5% gia mua vi đe chua neu cong thuc cu the.
        return self.purchase_price * 0.05


class Microphone(Device):
    def calculate_annual_maintenance_cost(self) -> float:
        # Tam dung 5% gia mua vi đe chua neu cong thuc cu the.
        return self.purchase_price * 0.05


class ProjectorRemote(Device):
    def calculate_annual_maintenance_cost(self) -> float:
        # Tam dung 5% gia mua vi đe chua neu cong thuc cu the.
        return self.purchase_price * 0.05
