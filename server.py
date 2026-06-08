from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import psutil
import time
from datetime import datetime
import json

class ServerMetrics:
    """جمع‌آوری اطلاعات سرور"""
    def __init__(self):
        self.cpu_usage = []
        self.memory_usage = []
        self.timestamp = []
        self.request_count = 0
        
    def record_metrics(self):
        """ثبت اطلاعات CPU و Memory"""
        self.cpu_usage.append(psutil.cpu_percent(interval=0.1))
        self.memory_usage.append(psutil.virtual_memory().percent)
        self.timestamp.append(datetime.now().strftime("%H:%M:%S"))
    
    def save_metrics(self, filename='metrics.json'):
        """ذخیره اطلاعات به فایل JSON"""
        data = {
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage,
            'timestamp': self.timestamp,
            'total_requests': self.request_count
        }
        with open(filename, 'w') as f:
            json.dump(data, f)
        print(f'✅ اطلاعات در فایل {filename} ذخیره شد')

class MyHandler(SimpleHTTPRequestHandler):
    """Handler برای درخواست‌های HTTP"""
    
    def do_GET(self):
        metrics.request_count += 1
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Server Response OK')
        
    def log_message(self, format, *args):
        """مخفی کردن log های پیش‌فرض"""
        pass

def monitor_server(interval=1):
    """نظارت بر عملکرد سرور"""
    print("\n📊 شروع نظارت بر سرور...")
    try:
        while True:
            metrics.record_metrics()
            print(f"CPU: {metrics.cpu_usage[-1]:.1f}% | Memory: {metrics.memory_usage[-1]:.1f}% | Requests: {metrics.request_count}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n🛑 نظارت متوقف شد")
        metrics.save_metrics()

metrics = ServerMetrics()

def start_server(port=8000):
    """شروع سرور HTTP"""
    server = HTTPServer(('localhost', port), MyHandler)
    print(f'✅ سرور در حال اجرا: http://localhost:{port}')
    print(f'⏰ زمان شروع: {datetime.now()}')
    
    # شروع نظارت در یک Thread جداگانه
    monitor_thread = threading.Thread(target=monitor_server, daemon=True)
    monitor_thread.start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n🛑 سرور متوقف شد')
        metrics.save_metrics()
        server.server_close()

if __name__ == '__main__':
    start_server()