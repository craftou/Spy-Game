from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
# إعداد السوكيت وتفعيل جدار الحماية للسماح بالاتصال
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    # صفحة ويب تستقبل البث وتحدث الصورة فوراً عبر الجافاسكريبت بدون إعادة تحميل
    html = '''
    <html>
        <head>
            <title>Spy-Game Ultimate Stream</title>
            <script src="https://socket.io"></script>
        </head>
        <body style="background:#121212; text-align:center; color:white; font-family:sans-serif; padding-top:20px;">
            <h1 style="color:#00ff88;">📡 Spy-Game Real-Time Stream</h1>
            <p>Status: <span id="status" style="color:red;">Disconnected</span></p>
            <hr style="border:1px solid #333; width:80%; mb:20px;">
            <img id="live-screen" style="max-width:85%; border:4px solid #00ff88; border-radius:8px; display:none;">
            <div id="waiting" style="padding: 50px; background:#1e1e1e; display:inline-block; border-radius:8px; border:1px dashed #555;">
                <p style="color:#aaa;">⏳ Waiting for stream data...</p>
            </div>

            <script>
                const socket = io();
                const img = document.getElementById('live-screen');
                const waiting = document.getElementById('waiting');
                const status = document.getElementById('status');

                socket.on('connect', () => { status.innerText = 'Connected'; status.style.color = '#00ff88'; });
                socket.on('disconnect', () => { status.innerText = 'Disconnected'; status.style.color = 'red'; });

                // استقبال الصورة وعرضها فوراً في نفس اللحظة
                socket.on('stream_update', (data) => {
                    waiting.style.display = 'none';
                    img.style.display = 'inline-block';
                    img.src = "data:image/jpeg;base64," + data.image;
                });
            </script>
        </body>
    </html>
    '''
    return render_template_string(html)

@socketio.on('video_stream')
def handle_stream(data):
    # إعادة توجيه الصورة القادمة من العميل إلى المتصفح فوراً
    emit('stream_update', {'image': data['image']}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=10000)
