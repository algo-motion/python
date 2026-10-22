# CLAUDE.md

File này hướng dẫn Claude Code (claude.ai/code) khi làm việc với code trong repository này.

## Tổng quan

Môt repo dùng để học python kết hợp với AWS. Repo này có các scipt python sử dụng boto3 để làm gọi đến các API của AWS

## Lệnh

Trên Windows, với virtualenv cục bộ trong `.venv/` (đã được gitignore):

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Nguyên tắc khi commit git

- Commit những file dùng chung cho cả dự án.
- Không commit những file cấu hình riêng cho từng người.
- Không commit những thư mục được sinh ra do cài đặt gói hoặc chạy script.

## Lưu ý

- Script dùng chuỗi credential mặc định của boto3 (biến môi trường / `~/.aws`); không có credential nào nằm trong repo. `.env` và `*.pem` đã được gitignore.
- `config.json` là cấu hình dùng chung của repo (được commit): trường `region` quy định region mặc định cho các script. Không commit secret vào file này.
