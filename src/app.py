import os
import socket
from flask import Flask, render_template
import redis

app = Flask(__name__)

# دریافت اطلاعات ردیس از متغیرهای محیطی
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# اتصال به ردیس با Fallback در صورت در دسترس نبودن
try:
    cache = redis.Redis(
        host=REDIS_HOST, 
        port=REDIS_PORT, 
        decode_responses=True, 
        socket_connect_timeout=1
    )
except Exception:
    cache = None

@app.route("/")
def index():
    visits = "Off"
    if cache:
        try:
            visits = cache.incr("page_views")
        except Exception:
            visits = "Offline"

    container_id = socket.gethostname()
    return render_template("index.html", visits=visits, container_id=container_id)

@app.route("/health")
def health():
    return {"status": "UP", "service": "python-backend"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)