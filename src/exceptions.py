"""Cac ngoai le nghiep vu cua quy trinh muon va tra thiet bi."""

from src.device import DeviceStatus


# Cac loi muon tra cu the ke thua tu ngoai le chung nay.
class BorrowingException(Exception):
    """Ngoai le co so cho cac loi nghiep vu muon-tra."""

    def __init__(self, message: str, inner_exception: Exception | None = None):
        super().__init__(message)
        self.inner_exception = inner_exception


# Loi nay xay ra khi thiet bi da duoc muon hoac dang bao tri.
class DeviceUnavailableException(BorrowingException):
    def __init__(self, device_id: str, current_status: DeviceStatus):
        self.device_id = device_id
        self.current_status = current_status
        super().__init__(
            f"Thiet bi '{device_id}' khong san sang; trang thai hien tai: "
            f"{current_status.value}."
        )


class BorrowLimitExceededException(BorrowingException):
    def __init__(self, borrower_id: str, maximum_devices: int):
        self.borrower_id = borrower_id
        self.maximum_devices = maximum_devices
        super().__init__(
            f"Nguoi muon '{borrower_id}' chi đuoc muon toi đa "
            f"{maximum_devices} thiet bi tren mot phieu."
        )


class InvalidBorrowPeriodException(BorrowingException):
    def __init__(self, device_id: str, requested_days: int, maximum_days: int):
        self.device_id = device_id
        self.requested_days = requested_days
        self.maximum_days = maximum_days
        super().__init__(
            f"Thoi han muon thiet bi '{device_id}' la {requested_days} ngay; "
            f"gioi han cho phep la {maximum_days} ngay."
        )


class DuplicateDeviceException(BorrowingException):
    def __init__(self, device_id: str):
        self.device_id = device_id
        super().__init__(f"Thiet bi '{device_id}' đa co trong phieu muon.")


class DeviceNotInSlipException(BorrowingException):
    def __init__(self, device_id: str):
        self.device_id = device_id
        super().__init__(f"Thiet bi '{device_id}' khong thuoc phieu muon.")


class DeviceAlreadyReturnedException(BorrowingException):
    def __init__(self, device_id: str):
        self.device_id = device_id
        super().__init__(f"Thiet bi '{device_id}' đa đuoc tra truoc đo.")


class InvalidReturnDateException(BorrowingException):
    def __init__(self, device_id: str, returned_date, borrowed_date):
        self.device_id = device_id
        self.returned_date = returned_date
        self.borrowed_date = borrowed_date
        super().__init__(
            f"Ngay tra thiet bi '{device_id}' khong đuoc truoc ngay muon."
        )
