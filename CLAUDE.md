# CLAUDE.md

File này hướng dẫn Claude Code (claude.ai/code) khi làm việc với code trong repository này.

## Tổng quan

Một repo nháp nhỏ gồm các script Python độc lập, gọi AWS qua `boto3`. Repo không có cấu trúc package, hệ thống build, bộ test hay linter. Mỗi script tự chứa và chạy từ trên xuống dưới ngay khi import (không có `main()` guard).

Hiện tại script duy nhất là `AWSS3Client.py`, liệt kê tên các S3 bucket ở region `ap-northeast-1`.

## Lệnh

Trên Windows, với virtualenv cục bộ trong `.venv/` (đã được gitignore):

```powershell
.venv\Scripts\Activate.ps1
python AWSS3Client.py
```

Script import `boto3` nhưng chưa có `requirements.txt`; nếu thiếu thì cài vào venv bằng `pip install boto3`.

## Lưu ý

- Script dùng chuỗi credential mặc định của boto3 (biến môi trường / `~/.aws`); không có credential nào nằm trong repo. `.env` và `*.pem` đã được gitignore.
- Region được ghi cứng trong từng script (`ap-northeast-1`).
