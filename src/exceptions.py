"""Các ngoại lệ nghiệp vụ của quy trình mượn và trả thiết bị."""

from src.device import DeviceStatus


class BorrowingException(Exception):
    """Ngoại lệ cơ sở cho các lỗi nghiệp vụ mượn-trả."""

    def __init__(self, message: str, inner_exception: Exception | None = None):
        super().__init__(message)
        self.inner_exception = inner_exception


class DeviceUnavailableException(BorrowingException):
    def __init__(self, device_id: str, current_status: DeviceStatus):
        self.device_id = device_id
        self.current_status = current_status
        super().__init__(
            f"Thiết bị '{device_id}' không sẵn sàng; trạng thái hiện tại: "
            f"{current_status.value}."
        )


class BorrowLimitExceededException(BorrowingException):
    def __init__(self, borrower_id: str, maximum_devices: int):
        self.borrower_id = borrower_id
        self.maximum_devices = maximum_devices
        super().__init__(
            f"Người mượn '{borrower_id}' chỉ được mượn tối đa "
            f"{maximum_devices} thiết bị trên một phiếu."
        )


class InvalidBorrowPeriodException(BorrowingException):
    def __init__(self, device_id: str, requested_days: int, maximum_days: int):
        self.device_id = device_id
        self.requested_days = requested_days
        self.maximum_days = maximum_days
        super().__init__(
            f"Thời hạn mượn thiết bị '{device_id}' là {requested_days} ngày; "
            f"giới hạn cho phép là {maximum_days} ngày."
        )


class DuplicateDeviceException(BorrowingException):
    def __init__(self, device_id: str):
        self.device_id = device_id
        super().__init__(f"Thiết bị '{device_id}' đã có trong phiếu mượn.")


class DeviceNotInSlipException(BorrowingException):
    def __init__(self, device_id: str):
        self.device_id = device_id
        super().__init__(f"Thiết bị '{device_id}' không thuộc phiếu mượn.")


class DeviceAlreadyReturnedException(BorrowingException):
    def __init__(self, device_id: str):
        self.device_id = device_id
        super().__init__(f"Thiết bị '{device_id}' đã được trả trước đó.")


class InvalidReturnDateException(BorrowingException):
    def __init__(self, device_id: str, returned_date, borrowed_date):
        self.device_id = device_id
        self.returned_date = returned_date
        self.borrowed_date = borrowed_date
        super().__init__(
            f"Ngày trả thiết bị '{device_id}' không được trước ngày mượn."
        )
