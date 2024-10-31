from flask import Flask, jsonify, request
import psycopg2
import redis
import os
from dotenv import load_dotenv

# Tải các biến môi trường từ file .env
load_dotenv()

app = Flask(__name__)

# Cấu hình kết nối PostgreSQL
postgres_host = os.getenv('POSTGRES_HOST')
postgres_db = os.getenv('POSTGRES_DB')
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')

# Cấu hình kết nối Redis
redis_host = os.getenv('REDIS_HOST')
redis_port = 6379

# Kết nối đến PostgreSQL
def get_postgres_connection():
    return psycopg2.connect(
        host=postgres_host,
        database=postgres_db,
        user=postgres_user,
        password=postgres_password
    )

# Kết nối đến Redis
redis_client = redis.Redis(host=redis_host, port=redis_port)

@app.route('/data', methods=['GET'])
def get_data():
    # Lấy dữ liệu từ Redis
    data = redis_client.get('my_key')
    if data:
        return jsonify({'source': 'redis', 'data': data.decode('utf-8')})
    
    # Nếu không có trong Redis, lấy từ PostgreSQL
    conn = get_postgres_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM your_table LIMIT 1;")
    row = cursor.fetchone()
    
    if row:
        # Lưu vào Redis
        redis_client.set('my_key', row[1])  # Giả định rằng giá trị cần lưu là cột thứ 2
        response = {'source': 'postgres', 'data': row[1]}
    else:
        response = {'message': 'No data found.'}

    cursor.close()
    conn.close()
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
