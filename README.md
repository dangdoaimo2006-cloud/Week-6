# Hệ thống quản lý thiết bị và hợp đồng bảo trì

Bài tập lập trình hướng đối tượng bằng Python. Dự án được triển khai theo từng lần code để dễ kiểm tra và commit lên GitHub.

## Cấu trúc hiện tại

```text
OOP_ThietBi_BaoTri/
├── README.md
├── docs/
│   └── 01-phan-tich-va-thiet-ke.md
├── src/
│   └── device.py
└── tests/
    └── test_device.py
```

## Tiến độ

### Lần code 1: Lớp thiết bị

- Xây dựng enum `DeviceStatus` gồm `AVAILABLE`, `BORROWED` và `UNDER_MAINTENANCE`.
- Xây dựng lớp trừu tượng `Device` với mã, tên, năm đưa vào sử dụng, giá mua và trạng thái.
- Kiểm tra mã và tên không được để trống, giá mua phải lớn hơn 0, năm đưa vào sử dụng không được ở tương lai.
- Mã thiết bị chỉ có thể đọc thông qua thuộc tính `device_id`, không có setter công khai.
- Xây dựng ba lớp `AirConditionerRemote`, `Microphone` và `ProjectorRemote`.
- Viết kiểm thử cho khởi tạo thiết bị, dữ liệu không hợp lệ, mã thiết bị, chi phí bảo trì và biểu diễn chuỗi.

**Lưu ý:** Đề chưa nêu công thức cụ thể để tính chi phí bảo trì hằng năm. Trong lần code này, tạm dùng 5% giá mua cho cả ba loại thiết bị để hoàn thiện cấu trúc phương thức; cần thay theo công thức của giảng viên nếu có quy định riêng.

## Chạy kiểm thử

Mở terminal tại thư mục dự án và chạy:

```bash
python -m unittest discover -s tests -v
```

## Commit lần code 1

```bash
git add README.md docs/01-phan-tich-va-thiet-ke.md src tests
git commit -m "Lan code 1: xay dung lop Device va cac loai thiet bi"
git push
```

## Các phần dự kiến triển khai tiếp theo

Các lần code sau sẽ tiếp tục xây dựng lớp phòng học, người mượn, chi tiết mượn, phiếu mượn, các ngoại lệ nghiệp vụ và kiểm thử các luồng mượn/trả thiết bị.
