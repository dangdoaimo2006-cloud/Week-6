from abc import ABC, abstractmethod
from datetime import date
from enum import Enum


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
    ):
        if not device_id or not device_id.strip():
            raise ValueError("Mã thiết bị không được để trống.")

        if not name or not name.strip():
            raise ValueError("Tên thiết bị không được để trống.")

        if purchase_price <= 0:
            raise ValueError("Giá mua phải lớn hơn 0.")

        if year_introduced > date.today().year:
            raise ValueError(
                "Năm đưa vào sử dụng không được lớn hơn năm hiện tại."
            )

        if not isinstance(status, DeviceStatus):
            raise TypeError("Trạng thái thiết bị không hợp lệ.")

        self._device_id = device_id.strip()
        self.name = name.strip()
        self.year_introduced = year_introduced
        self.purchase_price = float(purchase_price)
        self.status = status

    @property
    def device_id(self):
        return self._device_id

    @abstractmethod
    def calculate_annual_maintenance_cost(self) -> float:
        pass

    def __str__(self):
        return (
            f"Mã: {self.device_id}, "
            f"Tên: {self.name}, "
            f"Năm sử dụng: {self.year_introduced}, "
            f"Giá mua: {self.purchase_price:.2f}, "
            f"Trạng thái: {self.status.value}"
        )


class AirConditionerRemote(Device):
    def calculate_annual_maintenance_cost(self) -> float:
        # Tạm dùng 5% giá mua vì đề chưa nêu công thức cụ thể.
        return self.purchase_price * 0.05


class Microphone(Device):
    def calculate_annual_maintenance_cost(self) -> float:
        # Tạm dùng 5% giá mua vì đề chưa nêu công thức cụ thể.
        return self.purchase_price * 0.05


class ProjectorRemote(Device):
    def calculate_annual_maintenance_cost(self) -> float:
        # Tạm dùng 5% giá mua vì đề chưa nêu công thức cụ thể.
        return self.purchase_price * 0.05
