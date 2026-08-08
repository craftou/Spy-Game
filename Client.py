import socket
import pyautogui
import io
from PIL import Image
import struct
import time
import os

class Client:
    def __init__(self, server_ip, server_port=4444):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = None
    
    def connect(self):
        while True:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.server_ip, self.server_port))
                print("[+] Connected to server")
                self.send_screenshots()
            except Exception as e:
                print(f"[-] Connection failed: {e}")
                time.sleep(10)
    
    def capture_screen(self):
        screenshot = pyautogui.screenshot()
        img_bytes = io.BytesIO()
        screenshot.save(img_bytes, format='JPEG', quality=30)
        return img_bytes.getvalue()
    
    def send_screenshots(self):
        while True:
            try:
                img_data = self.capture_screen()
                size = len(img_data)
                self.socket.send(struct.pack('>I', size))
                self.socket.send(img_data)
                time.sleep(0.5)
            except Exception as e:
                print(f"[-] Error: {e}")
                self.socket.close()
                break

if __name__ == '__main__':
    server_ip = input("Enter server IP: ")
    client = Client(server_ip)
    client.connect()