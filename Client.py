import pyautogui
import io
import time
import requests

class Client:
    def __init__(self, server_url):
        # الرابط ينتهي بـ /upload لإرسال البيانات للـ API
        self.server_url = server_url.rstrip('/') + '/upload'
    
    def capture_screen(self):
        # التقاط الشاشة وضغطها بجودة 30% لتقليل استهلاك البيانات وسرعة النقل
        screenshot = pyautogui.screenshot()
        img_bytes = io.BytesIO()
        screenshot.save(img_bytes, format='JPEG', quality=30)
        return img_bytes.getvalue()
    
    def start_streaming(self):
        print("[+] Screen streaming started...")
        while True:
            try:
                img_data = self.capture_screen()
                
                # إرسال البيانات كملف مغلف برمجياً إلى السيرفر
                files = {'image': ('screen.jpg', img_data, 'image/jpeg')}
                response = requests.post(self.server_url, files=files, timeout=5)
                
                if response.status_code == 200:
                    print("[+] Screenshot sent successfully")
                else:
                    print(f"[-] Server returned error status: {response.status_code}")
                
                # إرسال لقطة كل ثانية (يمكنك تقليلها أو زيادتها)
                time.sleep(1)
                
            except Exception as e:
                print(f"[-] Connection failed or error occurred: {e}")
                time.sleep(5)  # الانتظار قبل إعادة المحاولة عند حدوث انقطاع

if __name__ == '__main__':
    # أدخل رابط موقعك على ريندر مثلاً: https://onrender.com
    url = input("Enter your Render Web App URL: ")
    client = Client(url)
    client.connect_url = url
    client.start_streaming()
