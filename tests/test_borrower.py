import unittest

from src.borrower import IBorrower, Lecturer, TeachingAssistant


class TestBorrower(unittest.TestCase):
    def test_create_lecturer(self):
        lecturer = Lecturer("GV01", "Nguyen Van An")

        self.assertEqual(lecturer.borrower_id, "GV01")
        self.assertEqual(lecturer.full_name, "Nguyen Van An")
        self.assertEqual(lecturer.get_maximum_devices(), 3)
        self.assertIsInstance(lecturer, IBorrower)

    def test_create_teaching_assistant(self):
        assistant = TeachingAssistant("TG01", "Tran Thi Binh")

        self.assertEqual(assistant.borrower_id, "TG01")
        self.assertEqual(assistant.full_name, "Tran Thi Binh")
        self.assertEqual(assistant.get_maximum_devices(), 2)
        self.assertIsInstance(assistant, IBorrower)

    def test_borrower_id_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            Lecturer("   ", "Nguyen Van An")

    def test_full_name_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            TeachingAssistant("TG01", " ")

    def test_borrower_information_is_trimmed(self):
        lecturer = Lecturer(" GV02 ", " Nguyen Van An ")

        self.assertEqual(lecturer.borrower_id, "GV02")
        self.assertEqual(lecturer.full_name, "Nguyen Van An")

    def test_string_representation(self):
        assistant = TeachingAssistant("TG02", "Le Minh")
        description = str(assistant)

        self.assertIn("TG02", description)
        self.assertIn("Le Minh", description)
        self.assertIn("2", description)


if __name__ == "__main__":
    unittest.main()
