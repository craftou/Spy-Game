import socket
import io
import struct
from PIL import Image
import cv2
import numpy as np

class Server:
    def __init__(self, port=4444):
        self.port = port
        self.server = None
        self.client = None
    
    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', self.port))
        self.server.listen(1)
        print(f"[+] Server listening on port {self.port}")
        
        self.client, addr = self.server.accept()
        print(f"[+] Client connected from {addr}")
        
        cv2.namedWindow('Remote Screen', cv2.WINDOW_NORMAL)
        
        while True:
            try:
                size_data = self.client.recv(4)
                if not size_data:
                    break
                size = struct.unpack('>I', size_data)[0]
                
                img_data = b''
                while len(img_data) < size:
                    chunk = self.client.recv(min(size - len(img_data), 4096))
                    if not chunk:
                        break
                    img_data += chunk
                
                img = Image.open(io.BytesIO(img_data))
                img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                cv2.imshow('Remote Screen', img_cv)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except Exception as e:
                print(f"[-] Error: {e}")
                break
        
        cv2.destroyAllWindows()
        self.client.close()
        self.server.close()

if __name__ == '__main__':
    Server().start()