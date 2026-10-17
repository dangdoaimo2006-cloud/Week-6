import unittest
from datetime import date

from src.device import (
    AirConditionerRemote,
    DeviceStatus,
    Microphone,
    ProjectorRemote,
)


class TestDevice(unittest.TestCase):
    def test_create_device(self):
        device = Microphone("MIC01", "Micro phong hoc", 2023, 1_000_000)

        self.assertEqual(device.device_id, "MIC01")
        self.assertEqual(device.name, "Micro phong hoc")
        self.assertEqual(device.status, DeviceStatus.AVAILABLE)

    def test_empty_device_id(self):
        with self.assertRaises(ValueError):
            Microphone("   ", "Micro phong hoc", 2023, 1_000_000)

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            Microphone("MIC01", "  ", 2023, 1_000_000)

    def test_purchase_price_must_be_positive(self):
        with self.assertRaises(ValueError):
            Microphone("MIC01", "Micro phong hoc", 2023, 0)

    def test_year_cannot_be_in_the_future(self):
        with self.assertRaises(ValueError):
            Microphone(
                "MIC01", "Micro phong hoc", date.today().year + 1, 1_000_000
            )

    def test_device_id_cannot_be_changed_through_property(self):
        device = Microphone("MIC01", "Micro phong hoc", 2023, 1_000_000)

        with self.assertRaises(AttributeError):
            device.device_id = "MIC02"

    def test_maintenance_cost(self):
        devices = [
            AirConditionerRemote("AC01", "Đieu khien đieu hoa", 2022, 200_000),
            Microphone("MIC01", "Micro phong hoc", 2023, 1_000_000),
            ProjectorRemote("PR01", "Đieu khien may chieu", 2021, 400_000),
        ]

        self.assertEqual(devices[0].calculate_annual_maintenance_cost(), 10_000)
        self.assertEqual(devices[1].calculate_annual_maintenance_cost(), 50_000)
        self.assertEqual(devices[2].calculate_annual_maintenance_cost(), 20_000)

    def test_string_representation(self):
        device = Microphone("MIC01", "Micro phong hoc", 2023, 1_000_000)

        self.assertIn("MIC01", str(device))
        self.assertIn("Micro phong hoc", str(device))
        self.assertIn("Available", str(device))


if __name__ == "__main__":
    unittest.main()
