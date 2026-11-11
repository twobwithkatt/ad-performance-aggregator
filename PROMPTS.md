# PROMPTS.md

### Prompt

input: file ad_data.csv dung lượng lớn
schema gồm các cột: campaign_id (string), date (YYYY-MM-DD), impressions (int), clicks (int), spend (float), conversions (int)

cần tính Aggregate theo campaign_id:
Tính tổng: total_impressions, total_clicks, total_spend, total_conversions

CTR = total_clicks / total_impressions (format 4 số thập phân)

CPA = total_spend / total_conversions (format 2 số thập phân, nếu conversions = 0 thì trả về null)

vì dataset lớn, cần chú ý tối ưu hiệu năng và mem, thiết kế kiến trúc hỗ trợ cả engine tốc độ cao lẫn fallback. Triển khai theo:

1. phân tích, vẽ flow, note lại yêu cầu, vẽ sơ đồ kiến trúc và luồng xử lý dữ liệu (memaid) lưu vào thư mục docs
2. viết test design/test cases chi tiết, bao quát các edge case lưu vào docs
3. impelment code theo TDD trong src, viết test suite bằng pytest trong tests trước, sau đó triển khai code nghiệp vụ để pass toàn bộ test
4. chạy toàn bộ coverage, chạy benchmark trực tiếp trên file ad_data.csv để đo thời gian thực thi và peak mem
5. tạo CLI cmd (ví dụ:  python aggregator.py --input ad_data.csv --output results), tạo Dockerfile, xuất 2 file kết quảtop10_ctr.csv: 10 chiến dịch có CTR cao nhất và top10_cpa.csv: 10 chiến dịch có CPA thấp nhất
6. viết lại README.md thành tài liệu hướng dẫn chạy (uv, pip, docker), giải thích kiến trúc và bổ sung bảng kết quả benchmark

máy có sẵn uv rồi, tạo .venv, tạo requirements.txt và cài đặt môi trường