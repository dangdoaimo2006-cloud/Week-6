from datetime import date

from src.device import Device, DeviceStatus


class ClassRoom:
    def __init__(self, room_id: str, name: str, capacity: int):
        if not room_id or not room_id.strip():
            raise ValueError("Mã phòng không được để trống.")

        if not name or not name.strip():
            raise ValueError("Tên phòng không được để trống.")

        if capacity <= 0:
            raise ValueError("Sức chứa phải lớn hơn 0.")

        self.room_id = room_id.strip()
        self.name = name.strip()
        self.capacity = capacity
        self.devices = []

    def add_device(self, device: Device) -> None:
        if device is None:
            raise ValueError("Không thể thêm thiết bị rỗng.")

        for current_device in self.devices:
            if current_device.device_id == device.device_id:
                raise ValueError("Phòng đã có thiết bị mang mã này.")

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
        total_cost = 0
        for device in self.devices:
            # Gọi phương thức của từng thiết bị, không cần xét loại thiết bị.
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
            f"Mã phòng: {self.room_id}, Tên phòng: {self.name}, "
            f"Sức chứa: {self.capacity}, Số thiết bị: {len(self.devices)}"
        )
