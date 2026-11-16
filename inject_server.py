from flask import Flask, request, render_template_string
import socket

app = Flask(__name__)

# قائمة لتخزين الرسائل أو التنبيهات
messages = ["مرحباً! تم الاتصال بنجاح. في انتظار الرسائل..."]

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

@app.route('/')
def index():
    html = '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>لوحة مراقبة الرسائل</title>
        <meta http-equiv="refresh" content="3">
        <style>
            body { background: #0f172a; color: #38bdf8; font-family: Tahoma, sans-serif; padding: 20px; }
            h2 { border-bottom: 2px solid #1e293b; padding-bottom: 10px; color: #f43f5e; }
            .box { background: #1e293b; padding: 15px; border-radius: 8px; margin-top: 15px; }
            ul { padding-right: 20px; }
            li { margin-bottom: 10px; background: #334155; padding: 10px; border-radius: 5px; color: #fff; }
        </style>
    </head>
    <body>
        <h2>📡 لوحة مراقبة الرسائل الحية</h2>
        <p>🔄 يتم تحديث الصفحة تلقائياً كل 3 ثوانٍ...</p>
        <div class="box">
            <h3>الرسائل الواردة:</h3>
            <ul>
            {% for m in messages %}
                <li>{{ m }}</li>
            {% endfor %}
            </ul>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, messages=messages)

@app.route('/push', methods=['POST'])
def push():
    data = request.json
    if data and 'msg' in data:
        messages.insert(0, data['msg'])
        return {"status": "success"}, 200
    return {"status": "fail"}, 400

if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 5000
    print(f"\n[+] السيرفر يعمل على: http://{local_ip}:{port}\n")
    app.run(host='0.0.0.0', port=port)
