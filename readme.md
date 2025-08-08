### Basic config
- thay đổi auth_url của cụm openstack trong app/config.py
- thay đổi endpoints của cụm openstack trong app/config.py (nếu khác mặc định)
- cấu hình redis_conn trong app/config.py
- cấu hình mongo_conn trong app/config.py
- cấu hình rabbitmq_config trong app/config.py
- cấu hình ip và id (channel_number) của client gọi tới IaC server
- thay đổi phần external_network_id của mục add router trong app/routes/infra/controllers.py

### docker
- cd docker/
- docker compose up --build -d

### Chạy server không qua docker
- cài terraform, redis, mongo, rabbitmq
- pip install -r requirements.txt
- cấu hình trong file config
- fastapi run .\app\app.py   

### Start queue worker
- huey_consumer app.core.queue.factories.huey_task.huey --logfile="./log/queue.log"

### Lưu ý
- Phía dùng api cần có webhook url để nhận thông báo hoặc kết nối với message queue
- Tạo client vdi (áp dụng tương tự với các client/app khác muốn kết nối tới IaC server)
    + rabbitmqctl add_user "192.168.239.1" "192.168.239.1"
    + rabbitmqctl set_permissions -p "/" "192.168.239.1" "" "" "^192.168.239.1_.*$"