from abc import ABC, abstractmethod


class IBorrower(ABC):
    """Giao dien mo ta cac thong tin chung cua nguoi muon thiet bi."""

    @property
    @abstractmethod
    def borrower_id(self) -> str:
        """Ma đinh danh nguoi muon."""
        raise NotImplementedError

    @property
    @abstractmethod
    def full_name(self) -> str:
        """Ho va ten nguoi muon."""
        raise NotImplementedError

    @abstractmethod
    def get_maximum_devices(self) -> int:
        """Tra ve so thiet bi toi đa đuoc muon tren mot phieu."""
        raise NotImplementedError


# Giang vien va tro giang dung chung cac thuoc tinh nhung co gioi han khac nhau.
class _BaseBorrower(IBorrower):
    """Lop co so dung chung phan thong tin cua nguoi muon."""

    MAXIMUM_DEVICES = 0

    def __init__(self, borrower_id: str, full_name: str):
        if not isinstance(borrower_id, str) or not borrower_id.strip():
            raise ValueError("Ma nguoi muon khong đuoc đe trong.")

        if not isinstance(full_name, str) or not full_name.strip():
            raise ValueError("Ho ten nguoi muon khong đuoc đe trong.")

        self._borrower_id = borrower_id.strip()
        self._full_name = full_name.strip()

    @property
    def borrower_id(self) -> str:
        return self._borrower_id

    @property
    def full_name(self) -> str:
        return self._full_name

    def get_maximum_devices(self) -> int:
        # Moi lop con tu khai bao gioi han MAXIMUM_DEVICES.
        return self.MAXIMUM_DEVICES

    def __str__(self) -> str:
        return (
            f"Ma nguoi muon: {self.borrower_id}, "
            f"Ho ten: {self.full_name}, "
            f"So thiet bi toi đa: {self.get_maximum_devices()}"
        )


class Lecturer(_BaseBorrower):
    """Giang vien đuoc muon toi đa 3 thiet bi tren mot phieu."""

    MAXIMUM_DEVICES = 3


class TeachingAssistant(_BaseBorrower):
    """Tro giang đuoc muon toi đa 2 thiet bi tren mot phieu."""

    MAXIMUM_DEVICES = 2
