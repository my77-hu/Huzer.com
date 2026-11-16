from flask import Flask, request, render_template_string
import socket

app = Flask(__name__)

# قائمة لتخزين الرسائل أو التنبيهات الواردة
messages = []

def get_local_ip():
    """الحصول تلقائياً على عنوان IP الخاص بالجهاز على شبكة الواي فاي"""
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
    # كود HTML و JavaScript محقون بالكامل ليعمل بمجرد فتح الرابط
    html = '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>لوحة المراقبة المحقونة</title>
        <style>
            body { background: #0f172a; color: #38bdf8; font-family: monospace; padding: 20px; }
            h2 { border-bottom: 2px solid #1e293b; padding-bottom: 10px; color: #f43f5e; }
            .box { background: #1e293b; padding: 15px; border-radius: 8px; margin-top: 15px; }
            .status { color: #4ade80; font-weight: bold; }
        </style>
        <script>
            // كود JavaScript محقون لضمان الاتصال والتحديث الفوري
            console.log("تم حقن سكريبت المراقبة بنجاح في متصفح الجوال المكسور.");
            setInterval(function() {
                // يمكنك هنا إضافة دوال لفحص أو إرسال حالة المتصفح دورياً للسيرفر
            }, 3000);
        </script>
    </head>
    <body>
        <h2>🛡️ لوحة التحكم والمراقبة النشطة</h2>
        <p>الحالة: <span class="status">متصل وجاهز للاستقبال</span></p>
        <div class="box">
            <h3>البيانات والرسائل المستقبلة:</h3>
            <ul id="msgList">
            {% for m in messages %}
                <li>{{ m }}</li>
            {% else %}
                <li>في انتظار تلقي البيانات...</li>
            {% endfor %}
            </ul>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, messages=messages)

@app.route('/inject-data', methods=['POST'])
def inject_data():
    """نقطة استقبال البيانات المحقونة من الأجهزة أو المتصفح"""
    data = request.json
    if data and 'payload' in data:
        messages.insert(0, data['payload'])
        return {"status": "injected_successfully"}, 200
    return {"status": "bad_request"}, 400

if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 5000
    print(codes := f"\n[+] السيرفر يعمل بنجاح!")
    print(f"[+] ارفع هذا الرابط وافتحه من المتصفح في الجوال المكسور:")
    print(f"👉   http://{local_ip}:{port}\n")
    app.run(host='0.0.0.0', port=port)
