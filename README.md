# App ghi chú local

Ứng dụng desktop nhỏ dùng Python, Tkinter và SQLite. Không cần Internet khi chạy.

## Cấu trúc

- `app.py`: giao diện và xử lý thao tác người dùng.
- `database.py`: tạo bảng, thêm, sửa, xóa và tìm dữ liệu.
- `notes.db`: tự sinh khi chạy lần đầu; đây là nơi lưu ghi chú.

## Chạy trên Windows

1. Cài Python 3 từ https://www.python.org/downloads/windows/
2. Trong màn hình cài đặt, chọn **Add python.exe to PATH**.
3. Mở PowerShell tại thư mục `note_app`.
4. Chạy:

   ```powershell
   python app.py
   ```

Nếu máy dùng Python Launcher, có thể chạy `py app.py`.

## Đóng gói thành file EXE

Trong thư mục `note_app`, chạy:

```powershell
python -m pip install pyinstaller
python -m PyInstaller --onefile --windowed --name LocalNotes app.py
```

File chạy nằm ở `dist/LocalNotes.exe`. Cơ sở dữ liệu `notes.db` sẽ nằm cạnh file EXE
khi ứng dụng được chạy từ thư mục đó.
"# note_app" 
