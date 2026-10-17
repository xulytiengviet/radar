# RADAR 24/7
Trung tâm tin tức công nghệ tiếng Việt do Long Ngo thiết kế. Dựa trên mẫu đính kèm **Radar Cộng Đồng AI (17/10/2026)**, giữ bốn cấu phần: dòng tin, bản đồ nhiệt chủ đề, phòng chiến lược đối thủ và bảng cơ hội.
## Triển khai
- Settings → Pages → Build and deployment → Deploy from a branch → main → /(root) → Save.
- Actions → Update RADAR RSS → Run workflow để khởi tạo nguồn tin.
- Website: https://xulytiengviet.github.io/radar/
- Nếu Actions không thể git push, bật Settings → Actions → General → Workflow permissions → Read and write permissions, nếu có quyền cấu hình.
## Kiến trúc
Python thư viện chuẩn thu thập RSS công khai (Google News RSS), xuất data/news.json; workflow được lên lịch 30 phút (lịch GitHub Actions không bảo đảm chạy chính xác); giao diện HTML/CSS/JS đọc file JSON và kiểm tra lại mỗi 5 phút. Giữ tối đa 500 bài, kèm nguồn và thời gian đăng. Không cần API key, không đòi máy chủ riêng.
Phân loại chủ đề, số lượt nhắc tổ chức, cơ hội nghiên cứu dựa vào truy vấn / từ khóa, **không phải** kết luận cạnh tranh hoặc dự báo được kiểm chứng. Bản quyền bài báo thuộc nhà xuất bản, mã nguồn phần mềm MIT.
