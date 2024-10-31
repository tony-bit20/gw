# Sử dụng Python 3.9
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép yêu cầu vào container
COPY requirements.txt .

# Cài đặt yêu cầu
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn vào container
COPY app.py .

# Chạy ứng dụng
CMD ["python", "app.py"]
