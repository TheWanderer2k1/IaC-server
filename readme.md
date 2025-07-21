### Quick start server
fastapi run .\app\app.py   

### Start queue worker
huey_consumer app.config.huey --logfile=queue.log 

### Lưu ý
Phía dùng api cần có webhook url để nhận thông báo