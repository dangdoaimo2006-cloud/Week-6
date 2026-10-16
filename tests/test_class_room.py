import unittest
from datetime import date

from src.class_room import ClassRoom
from src.device import (
    AirConditionerRemote,
    DeviceStatus,
    Microphone,
    ProjectorRemote,
)


class TestClassRoom(unittest.TestCase):
    def setUp(self):
        self.room = ClassRoom("P101", "Phòng học 101", 40)
        self.microphone = Microphone("MIC01", "Micro phòng học", 2023, 1_000_000)
        self.remote = AirConditionerRemote(
            "AC01", "Điều khiển điều hòa", 2018, 200_000
        )

    def test_create_class_room(self):
        self.assertEqual(self.room.room_id, "P101")
        self.assertEqual(self.room.name, "Phòng học 101")
        self.assertEqual(self.room.capacity, 40)
        self.assertEqual(len(self.room.devices), 0)

    def test_add_and_find_device(self):
        self.room.add_device(self.microphone)
        self.assertIs(self.room.find_device("MIC01"), self.microphone)
        self.assertIsNone(self.room.find_device("UNKNOWN"))

    def test_cannot_add_none(self):
        with self.assertRaises(ValueError):
            self.room.add_device(None)

    def test_cannot_add_duplicate_device_id(self):
        self.room.add_device(self.microphone)
        another_microphone = Microphone(
            "MIC01", "Micro khác", 2024, 800_000
        )
        with self.assertRaises(ValueError):
            self.room.add_device(another_microphone)

    def test_remove_device(self):
        self.room.add_device(self.microphone)
        self.assertTrue(self.room.remove_device("MIC01"))
        self.assertFalse(self.room.remove_device("MIC01"))
        self.assertEqual(len(self.room.devices), 0)

    def test_calculate_maintenance_cost_using_polymorphism(self):
        self.room.add_device(self.microphone)
        self.room.add_device(self.remote)
        self.assertEqual(
            self.room.calculate_annual_maintenance_cost(), 60_000
        )

    def test_devices_requiring_maintenance(self):
        old_device = self.remote
        device_under_maintenance = ProjectorRemote(
            "PR01", "Điều khiển máy chiếu", date.today().year, 400_000,
            DeviceStatus.UNDER_MAINTENANCE,
        )
        new_device = Microphone("MIC02", "Micro mới", date.today().year, 500_000)

        self.room.add_device(old_device)
        self.room.add_device(device_under_maintenance)
        self.room.add_device(new_device)

        result = self.room.get_devices_requiring_maintenance()
        self.assertIn(old_device, result)
        self.assertIn(device_under_maintenance, result)
        self.assertNotIn(new_device, result)

    def test_invalid_room_data(self):
        with self.assertRaises(ValueError):
            ClassRoom("", "Phòng học", 30)
        with self.assertRaises(ValueError):
            ClassRoom("P102", "Phòng học", 0)


if __name__ == "__main__":
    unittest.main()
