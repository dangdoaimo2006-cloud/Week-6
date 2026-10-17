# Hệ thống quản lý thiết bị và mượn thiết bị

Chương trình Python mô phỏng việc quản lý thiết bị phục vụ giảng dạy, phòng học, người mượn và quy trình mượn–trả thiết bị. Dự án được triển khai theo từng giai đoạn để bám sát yêu cầu trong `lab w06.pdf`.

## Chức năng

- Quản lý thiết bị: điều khiển điều hòa, micro và điều khiển máy chiếu; trạng thái thiết bị; thời hạn mượn tối đa.
- Quản lý phòng học: thêm, xóa, tìm thiết bị; tính chi phí bảo trì theo tính đa hình; lọc thiết bị cần bảo trì.
- Quản lý người mượn: `Lecturer` được mượn tối đa 3 thiết bị trên một phiếu; `TeachingAssistant` được mượn tối đa 2.
- Quản lý mục mượn `BorrowItem`: ngày mượn, hạn trả, tiết mượn và ngày trả.
- Quản lý phiếu mượn `BorrowingSlip`: thêm thiết bị, trả thiết bị, tính phí trả muộn và liệt kê mục mượn chưa trả hoặc trả muộn.
- Ngoại lệ nghiệp vụ: thiết bị không sẵn sàng, vượt giới hạn người mượn, thời hạn mượn không hợp lệ, thiết bị trùng, thiết bị không thuộc phiếu, thiết bị đã trả và ngày trả không hợp lệ.
- Kiểm thử bằng thư viện chuẩn `unittest`.

## Cấu trúc dự án

```text
w06/
├── README.md
├── docs/
│   └── 01-phan-tich-va-thiet-ke.md
├── src/
│   ├── device.py
│   ├── class_room.py
│   ├── borrower.py
│   ├── borrow_item.py
│   ├── exceptions.py
│   └── borrowing_slip.py
└── tests/
    ├── test_device.py
    ├── test_class_room.py
    ├── test_borrower.py
    ├── test_borrow_item.py
    └── test_borrowing_slip.py
```

## Yêu cầu môi trường

- Python 3.10 trở lên.
- Không cần cài thư viện bên ngoài.

Kiểm tra phiên bản Python:

```bash
python --version
```

## Chạy kiểm thử

Mở terminal tại thư mục gốc `w06` và chạy:

```bash
python -m unittest discover -s tests -v
```

## Ví dụ sử dụng

```python
from datetime import date

from src.borrower import Lecturer
from src.borrowing_slip import BorrowingSlip
from src.device import Microphone

borrower = Lecturer("GV01", "Nguyen Van A")
device = Microphone(
    "MIC01", "Micro phong hoc", 2023, 1_000_000,
    max_borrow_days=1,
)
slip = BorrowingSlip("PM01", borrower, "P101", date(2026, 10, 1))
slip.add_device(device, borrow_days=1)
fee = slip.return_device("MIC01", date(2026, 10, 3))
print(fee)
```

## Các giả định triển khai cần biết

- Đề bài yêu cầu thời hạn mượn tối đa của từng thiết bị nhưng không quy định giá trị mặc định. Trong chương trình, `max_borrow_days` mặc định bằng 1 ngày; có thể truyền giá trị khác khi khởi tạo thiết bị.
- Đề bài chưa nêu công thức hoặc mức phí trả muộn. Chương trình tạm dùng `BorrowingSlip.LATE_FEE_PER_DAY = 10000` (đơn vị tiền tệ theo bài tập) cho mỗi ngày trễ. Có thể thay đổi hằng số hoặc truyền `late_fee_per_day` khi tạo phiếu.
- Chi phí bảo trì hằng năm hiện được tính bằng 5% giá mua cho cả ba loại thiết bị vì đề chưa chỉ định công thức. Đây là giả định triển khai, không phải quy tắc được nêu trong đề.
- `BorrowItem` lưu khoảng tiết mượn và hạn trả theo ngày. `BorrowingSlip.add_device()` nhận số ngày mượn; khoảng tiết trong mục được đặt mặc định là tiết 1 đến tiết 1 vì chữ ký phương thức trong đề không truyền thông tin tiết.
- Các phương thức Python dùng `snake_case`; một số alias viết theo PascalCase được giữ để tiện đối chiếu chữ ký C# trong đề.

## Tài liệu

Xem [`docs/01-phan-tich-va-thiet-ke.md`](docs/01-phan-tich-va-thiet-ke.md) để đọc phân tích yêu cầu và thiết kế sơ bộ.
