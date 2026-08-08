from flask import Flask, request, render_template_string
import base64

app = Flask(__name__)

# متغير لحفظ آخر صورة مستلمة في ذاكرة السيرفر
last_image_b64 = ""

@app.route('/upload', methods=['POST'])
def upload():
    global last_image_b64
    # استقبال ملف الصورة من العميل
    file = request.files.get('image')
    if file:
        img_bytes = file.read()
        # تحويل الصورة إلى نص b64 ليتم عرضها بسهولة في المتصفح
        last_image_b64 = base64.b64encode(img_bytes).decode('utf-8')
        return "OK", 200
    return "No Image", 400

@app.route('/')
def index():
    # صفحة ويب بسيطة بتصميم داكن تقوم بتحديث نفسها تلقائياً
    html = '''
    <html>
        <head>
            <title>Remote Screen Live</title>
            <meta http-equiv="refresh" content="1">
        </head>
        <body style="background:#121212; text-align:center; color:white; font-family:sans-serif; padding-top:30px;">
            <h1 style="color:#00ff88;">📡 Spy-Game Live Screen</h1>
            <p>The page refreshes every 1 second automatically.</p>
            <hr style="border:1px solid #333; width:80%;">
            <br>
            {% if img %}
                <img src="data:image/jpeg;base64,{{ img }}" style="max-width:85%; border:4px solid #00ff88; border-radius:8px; box-shadow: 0px 0px 20px #00ff8855;">
            {% else %}
                <div style="padding: 50px; background:#1e1e1e; display:inline-block; border-radius:8px; border:1px dashed #555;">
                    <p style="color:#aaa;">⏳ Waiting for connection / client screenshots...</p>
                </div>
            {% endif %}
        </body>
    </html>
    '''
    return render_template_string(html, img=last_image_b64)

if __name__ == '__main__':
    # المنفذ الافتراضي لمنصة Render هو 10000
    app.run(host='0.0.0.0', port=10000)
