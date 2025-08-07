### Quick start server
fastapi run .\app\app.py   

### Start queue worker
huey_consumer app.core.queue.factories.huey_task.huey --logfile="./log/queue.log"

### docker
cd docker/
docker compose up --build -d

### Lưu ý
- Phía dùng api cần có webhook url để nhận thông báo hoặc kết nối với message queue
- Tạo vdi (áp dụng tương tự với các client/app khác muốn kết nối tới IaC server)
    rabbitmqctl add_user "vdi" "vdi"
    rabbitmqctl set_permissions -p "/" "vdi" "" "" "^vdi_.*$"