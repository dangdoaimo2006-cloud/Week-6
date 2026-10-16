from abc import ABC, abstractmethod


class IBorrower(ABC):
    """Giao diện mô tả các thông tin chung của người mượn thiết bị."""

    @property
    @abstractmethod
    def borrower_id(self) -> str:
        """Mã định danh người mượn."""
        raise NotImplementedError

    @property
    @abstractmethod
    def full_name(self) -> str:
        """Họ và tên người mượn."""
        raise NotImplementedError

    @abstractmethod
    def get_maximum_devices(self) -> int:
        """Trả về số thiết bị tối đa được mượn trên một phiếu."""
        raise NotImplementedError


class _BaseBorrower(IBorrower):
    """Lớp cơ sở dùng chung phần thông tin của người mượn."""

    MAXIMUM_DEVICES = 0

    def __init__(self, borrower_id: str, full_name: str):
        if not isinstance(borrower_id, str) or not borrower_id.strip():
            raise ValueError("Mã người mượn không được để trống.")

        if not isinstance(full_name, str) or not full_name.strip():
            raise ValueError("Họ tên người mượn không được để trống.")

        self._borrower_id = borrower_id.strip()
        self._full_name = full_name.strip()

    @property
    def borrower_id(self) -> str:
        return self._borrower_id

    @property
    def full_name(self) -> str:
        return self._full_name

    def get_maximum_devices(self) -> int:
        return self.MAXIMUM_DEVICES

    def __str__(self) -> str:
        return (
            f"Mã người mượn: {self.borrower_id}, "
            f"Họ tên: {self.full_name}, "
            f"Số thiết bị tối đa: {self.get_maximum_devices()}"
        )


class Lecturer(_BaseBorrower):
    """Giảng viên được mượn tối đa 3 thiết bị trên một phiếu."""

    MAXIMUM_DEVICES = 3


class TeachingAssistant(_BaseBorrower):
    """Trợ giảng được mượn tối đa 2 thiết bị trên một phiếu."""

    MAXIMUM_DEVICES = 2
