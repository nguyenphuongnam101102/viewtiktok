# TikTok Auto Tools

Công cụ tự động hóa cho TikTok (View, Like, Follow) và các mạng xã hội khác.

## Cài đặt

```bash
pip install -r requirements.txt
```

## Lấy API Token

- **likevn.py & followtiktok.py**: [Lấy API token tại đây](https://like.vn/docs/api)
- **chaysubvn.py**: [Lấy API token tại đây](https://chaysub.vn/docs-api-v2)

## Sử dụng

### 1. likevn.py - Tổng hợp công cụ
```bash
python likevn.py
```
Hỗ trợ: View TikTok, Like TikTok, Follow TikTok, Like Facebook, Like Instagram

### 2. followtiktok.py - Tăng Follow TikTok
```bash
python followtiktok.py
```

### 3. chaysubvn.py - Tăng View TikTok
```bash
python chaysubvn.py
```

## Lưu ý

- API token sẽ được lưu tự động vào file cấu hình
- Các file `api_token*.txt` đã được thêm vào `.gitignore`
