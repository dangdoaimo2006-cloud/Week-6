# Hệ thống quản lý thiết bị và mượn thiết bị — W06

Dự án Python hướng đối tượng cho bài Lab W06. Đây là bản tổng hợp cuối cùng của các phần đã triển khai: thiết bị, phòng học, người mượn, mục mượn, phiếu mượn và ngoại lệ nghiệp vụ.

## Chức năng chính

- `Device` là lớp trừu tượng; ba loại thiết bị gồm `AirConditionerRemote`, `Microphone`, `ProjectorRemote`.
- `DeviceStatus` quản lý ba trạng thái `Available`, `Borrowed`, `UnderMaintenance`.
- `ClassRoom` quản lý thiết bị, tìm/xóa thiết bị, tính chi phí bảo trì bằng tính đa hình và lọc thiết bị cần bảo trì.
- `Lecturer` được mượn tối đa 3 thiết bị trên một phiếu; `TeachingAssistant` tối đa 2.
- `BorrowItem` lưu thông tin mượn, hạn trả và ngày trả.
- `BorrowingSlip` kiểm tra điều kiện trước khi thay đổi trạng thái thiết bị, xử lý mượn/trả và tính phí trả muộn.
- Các ngoại lệ nghiệp vụ được khai báo trong `src/exceptions.py`.
- Bộ kiểm thử đơn vị và tích hợp dùng `unittest`, không cần thư viện ngoài.

## Cấu trúc

```text
w06/
├── README.md
├── docs/01-phan-tich-va-thiet-ke.md
├── src/
│   ├── __init__.py
│   ├── device.py
│   ├── class_room.py
│   ├── borrower.py
│   ├── borrow_item.py
│   ├── exceptions.py
│   └── borrowing_slip.py
└── tests/
    ├── __init__.py
    ├── test_device.py
    ├── test_class_room.py
    ├── test_borrower.py
    ├── test_borrow_item.py
    ├── test_borrowing_slip.py
    └── test_integration.py
```

## Yêu cầu và cách chạy

Yêu cầu Python 3.10 trở lên. Mở terminal tại thư mục `w06` (thư mục chứa `README.md`) và chạy:

```bash
python -m unittest discover -s tests -v
```

Chạy một nhóm kiểm thử riêng, ví dụ:

```bash
python -m unittest tests.test_integration -v
```

## Các giả định triển khai

Đề bài không quy định công thức chi phí bảo trì, mức phí trả muộn hoặc thời hạn mượn mặc định. Vì vậy, chương trình dùng các giả định sau; cần điều chỉnh nếu giảng viên cung cấp quy tắc khác:

- Chi phí bảo trì hằng năm = 5% giá mua của thiết bị.
- Phí trả muộn mặc định = 10.000 cho mỗi ngày trễ; có thể truyền `late_fee_per_day` khi tạo `BorrowingSlip`.
- `max_borrow_days` mặc định là 1 ngày; có thể cấu hình khi tạo thiết bị.
- Vì `add_device()` nhận số ngày chứ không nhận khoảng tiết, `BorrowItem` đặt khoảng tiết mặc định từ tiết 1 đến tiết 1.

Các giả định trên là lựa chọn triển khai, không được xem là công thức bắt buộc từ đề bài.

## Gợi ý commit cuối

```bash
git add README.md src tests
git commit -m "Hoàn thiện kiểm thử tích hợp và rà soát dự án W06"
git push origin main
```
