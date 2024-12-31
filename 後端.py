from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# 初始化數據庫
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            course_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()

    if user:
        # 返回可用課程
        c.execute('SELECT id, name, price FROM courses')
        courses = [{"id": row[0], "name": row[1], "price": row[2]} for row in c.fetchall()]
        return jsonify({"message": "登入成功", "courses": courses})
    else:
        return jsonify({"message": "登入失敗"}), 401

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.json
    course_id = data.get('courseId')

    # 假設用戶 ID 是 1（這裡需要根據 session 獲取用戶 ID）
    user_id = 1

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO cart (user_id, course_id) VALUES (?, ?)', (user_id, course_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "課程已加入購物車！"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
