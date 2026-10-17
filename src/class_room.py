from datetime import date

from src.device import Device, DeviceStatus


class ClassRoom:
    def __init__(self, room_id: str, name: str, capacity: int):
        if not room_id or not room_id.strip():
            raise ValueError("Ma phong khong đuoc đe trong.")

        if not name or not name.strip():
            raise ValueError("Ten phong khong đuoc đe trong.")

        if capacity <= 0:
            raise ValueError("Suc chua phai lon hon 0.")

        self.room_id = room_id.strip()
        self.name = name.strip()
        self.capacity = capacity
        # Danh sach don gian la du dung cho pham vi bai tap nay.
        self.devices = []

    def add_device(self, device: Device) -> None:
        if device is None:
            raise ValueError("Khong the them thiet bi rong.")

        # Kiem tra ma truoc de tranh them trung mot thiet bi.
        for current_device in self.devices:
            if current_device.device_id == device.device_id:
                raise ValueError("Phong đa co thiet bi mang ma nay.")

        self.devices.append(device)

    def remove_device(self, device_id: str) -> bool:
        device = self.find_device(device_id)
        if device is None:
            return False

        self.devices.remove(device)
        return True

    def find_device(self, device_id: str):
        for device in self.devices:
            if device.device_id == device_id:
                return device
        return None

    def calculate_annual_maintenance_cost(self) -> float:
        # Moi lop con tu tinh chi phi cua minh thong qua da hinh.
        total_cost = 0
        for device in self.devices:
            # Goi phuong thuc cua tung thiet bi, khong can xet loai thiet bi.
            total_cost += device.calculate_annual_maintenance_cost()
        return total_cost

    def get_devices_requiring_maintenance(self):
        current_year = date.today().year
        result = []

        for device in self.devices:
            used_years = current_year - device.year_introduced
            if (
                device.status == DeviceStatus.UNDER_MAINTENANCE
                or used_years > 5
            ):
                result.append(device)

        return result

    def __str__(self):
        return (
            f"Ma phong: {self.room_id}, Ten phong: {self.name}, "
            f"Suc chua: {self.capacity}, So thiet bi: {len(self.devices)}"
        )
