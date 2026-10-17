# Hệ thống quản lý thiết bị và mượn thiết bị

Chương trình được xây dựng bằng Python để thực hành lập trình hướng đối tượng (OOP). Bài tập mô phỏng việc quản lý thiết bị phục vụ giảng dạy, phòng học và quy trình mượn – trả thiết bị tại trường đại học.

> **Tiến độ hiện tại:** Đã hoàn thành lần code 1 (các lớp thiết bị), lần code 2 (lớp phòng học), lần code 3 (người mượn) và lần code 4 (`BorrowItem`). Lớp phiếu mượn và ngoại lệ nghiệp vụ sẽ được bổ sung ở giai đoạn tiếp theo.

## Mục tiêu

- Áp dụng lớp trừu tượng, kế thừa, ghi đè phương thức và tính đa hình.
- Quản lý thông tin thiết bị và danh sách thiết bị trong phòng học.
- Kiểm tra dữ liệu đầu vào theo các điều kiện của đề bài.
- Viết kiểm thử đơn vị cho những chức năng đã triển khai.

## Chức năng đã triển khai

### 1. Quản lý thiết bị

- Lớp trừu tượng `Device` lưu mã, tên, năm đưa vào sử dụng, giá mua và trạng thái.
- Ba lớp thiết bị: `AirConditionerRemote`, `Micro` (`Microphone` trong code) và `ProjectorRemote`.
- Mã thiết bị được thiết lập khi khởi tạo; kiểm tra mã và tên không rỗng, giá mua lớn hơn 0, năm sử dụng không vượt quá năm hiện tại.
- Mỗi loại thiết bị triển khai phương thức tính chi phí bảo trì dự kiến hằng năm.

### 2. Quản lý phòng học

- Lớp `ClassRoom` lưu mã phòng, tên phòng, sức chứa và danh sách thiết bị.
- Thêm thiết bị, xóa thiết bị theo mã và tìm thiết bị theo mã.
- Tính tổng chi phí bảo trì thông qua phương thức của từng thiết bị (đa hình).
- Lọc thiết bị đang ở trạng thái `UNDER_MAINTENANCE` hoặc đã được sử dụng trên 5 năm.
- Không cho thêm thiết bị rỗng hoặc thiết bị có mã trùng trong cùng phòng.

### 3. Quản lý người mượn

- `IBorrower` định nghĩa các thông tin và hành vi chung của người mượn.
- `Lecturer` đại diện cho giảng viên, được mượn tối đa 3 thiết bị trên một phiếu.
- `TeachingAssistant` đại diện cho trợ giảng, được mượn tối đa 2 thiết bị trên một phiếu.
- Mã người mượn và họ tên không được để trống; khoảng trắng ở đầu và cuối được loại bỏ.

### 4. Chi tiết mượn thiết bị (`BorrowItem`)

- Lưu thiết bị, ngày mượn, tiết bắt đầu, tiết kết thúc và ngày trả.
- Kiểm tra thiết bị không rỗng; các tiết phải là số nguyên dương và tiết kết thúc không đứng trước tiết bắt đầu.
- Ngày trả ban đầu là `None`; chỉ ghi nhận trả khi ngày trả không trước ngày mượn.
- Không cho phép ghi nhận trả lần thứ hai cho cùng một mục mượn.

## Cấu trúc thư mục

```text
w06/
├── README.md
├── docs/
│   └── 01-phan-tich-va-thiet-ke.md
├── src/
│   ├── device.py
│   ├── class_room.py
│   └── borrower.py
└── tests/
    ├── test_device.py
    └── test_class_room.py
```

## Yêu cầu môi trường

- Python 3.10 trở lên được khuyến nghị.
- Không cần cài thêm thư viện bên ngoài; chương trình sử dụng thư viện chuẩn `unittest` để kiểm thử.

Kiểm tra phiên bản Python:

```bash
python --version
```

## Cách chạy kiểm thử

Mở terminal tại thư mục gốc `w06`, sau đó chạy:

```bash
python -m unittest discover -s tests -v
```

Lệnh trên tự động tìm các file kiểm thử có tên bắt đầu bằng `test_` trong thư mục `tests`.

## Những điểm cần lưu ý

- Đề bài chưa quy định công thức tính chi phí bảo trì. Trong phiên bản hiện tại, cả ba loại thiết bị đang tạm tính chi phí bằng **5% giá mua**. Đây là giả định triển khai, không phải công thức được nêu rõ trong đề; cần điều chỉnh nếu giảng viên cung cấp quy tắc khác.
- Các lớp và tên phương thức đang dùng quy ước đặt tên Python (`snake_case`).
- Quy tắc giới hạn số thiết bị đã được khai báo trong từng loại người mượn; việc áp dụng giới hạn này khi tạo phiếu sẽ được thực hiện trong phần `BorrowingSlip`. Lớp `BorrowItem` đã ghi nhận ngày mượn/trả và các tiết mượn; việc kiểm tra giới hạn mượn theo từng loại thiết bị, đổi trạng thái thiết bị và tính phí trễ sẽ được phối hợp ở `BorrowingSlip`. Hệ thống ngoại lệ nghiệp vụ chưa được triển khai.

## Kế hoạch phát triển tiếp theo

1. Xây dựng `BorrowingSlip` cùng các quy tắc mượn – trả và ngoại lệ nghiệp vụ.
2. Bổ sung tính phí trả muộn và kiểm tra trạng thái thiết bị trong quy trình mượn – trả.
3. Bổ sung kiểm thử tích hợp cho các luồng thành công và các trường hợp phát sinh ngoại lệ theo đề bài.

## Tài liệu

Tài liệu phân tích yêu cầu và thiết kế sơ bộ nằm tại [`docs/01-phan-tich-va-thiet-ke.md`](docs/01-phan-tich-va-thiet-ke.md).
