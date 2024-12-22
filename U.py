from flask import Flask, render_template_string, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# تهيئة قاعدة البيانات
def init_db():
    conn = sqlite3.connect('rezdar_financial.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('rezdar', '1234'))
    conn.commit()
    conn.close()

# صفحة تسجيل الدخول
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # التحقق من المستخدم وكلمة المرور
        conn = sqlite3.connect('rezdar_financial.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return redirect(url_for("dashboard"))
        else:
            flash("اسم المستخدم أو كلمة المرور غير صحيحة", "error")
    return render_template_string(HTML_TEMPLATE)

# صفحة اللوحة الرئيسية بعد تسجيل الدخول
@app.route("/dashboard")
def dashboard():
    return render_template_string(DASHBOARD_TEMPLATE)

# إعداد قاعدة البيانات عند تشغيل التطبيق لأول مرة
@app.before_first_request
def before_first_request():
    init_db()

# HTML و CSS مدمجان داخل الكود
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>خدمات ريزدار المالية - تسجيل الدخول</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }

        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.3);
        }

        .login-box {
            background: linear-gradient(135deg, #7a4f98, #1c92d2);
            border-radius: 15px;
            padding: 40px 50px;
            text-align: center;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
            transform: translateY(-10px);
            transition: all 0.3s ease;
        }

        .login-box:hover {
            transform: translateY(0);
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.3);
        }

        h2 {
            color: #fff;
            margin-bottom: 20px;
            font-size: 24px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .textbox {
            position: relative;
            margin-bottom: 20px;
        }

        .textbox input {
            width: 100%;
            padding: 10px;
            padding-left: 40px;
            background: #fff;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            color: #333;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            transition: 0.3s;
        }

        .textbox input:focus {
            outline: none;
            box-shadow: 0 0 10px rgba(0, 0, 255, 0.5);
        }

        .textbox input::placeholder {
            color: #888;
        }

        input[type="submit"] {
            width: 100%;
            padding: 10px;
            border: none;
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            cursor: pointer;
            transition: 0.3s;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

        input[type="submit"]:hover {
            background-color: #45a049;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
        }

        .error-message {
            color: red;
            font-size: 14px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <h2>تسجيل الدخول</h2>
            <form action="/" method="POST">
                <div class="textbox">
                    <input type="text" placeholder="اسم المستخدم" name="username" required>
                </div>
                <div class="textbox">
                    <input type="password" placeholder="كلمة المرور" name="password" required>
                </div>
                <input type="submit" value="تسجيل الدخول">
            </form>
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    <div class="error-message">
                        {% for category, message in messages %}
                            <p>{{ message }}</p>
                        {% endfor %}
                    </div>
                {% endif %}
            {% endwith %}
        </div>
    </div>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة التحكم</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }

        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.3);
        }

        .login-box {
            background: linear-gradient(135deg, #7a4f98, #1c92d2);
            border-radius: 15px;
            padding: 40px 50px;
            text-align: center;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
            transform: translateY(-10px);
            transition: all 0.3s ease;
        }

        .login-box:hover {
            transform: translateY(0);
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.3);
        }

        h2 {
            color: #fff;
            margin-bottom: 20px;
            font-size: 24px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        p {
            color: white;
            font-size: 18px;
            margin-bottom: 20px;
        }

        a {
            color: #fff;
            font-size: 16px;
            text-decoration: none;
            border: 2px solid #fff;
            padding: 10px 20px;
            border-radius: 5px;
            display: inline-block;
        }

        a:hover {
            background-color: #fff;
            color: #1c92d2;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <h2>مرحبًا بك في لوحة التحكم</h2>
            <p>لقد تم تسجيل الدخول بنجاح</p>
            <a href="/">تسجيل الخروج</a>
        </div>
    </div>
</body>
</html>
'''

if __name__ == "__main__":
    app.run(debug=True)
