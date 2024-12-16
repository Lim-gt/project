from flask import Flask
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('gyeongtaekdb.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS a (id INTEGER PRIMARY KEY, count INTEGER DEFAULT 0)')
    cursor.execute('CREATE TABLE IF NOT EXISTS b (id INTEGER PRIMARY KEY, count INTEGER DEFAULT 0)')
    cursor.execute('CREATE TABLE IF NOT EXISTS c (id INTEGER PRIMARY KEY, count INTEGER DEFAULT 0)')
    cursor.execute('INSERT OR IGNORE INTO a (id, count) VALUES (1, 0)')
    cursor.execute('INSERT OR IGNORE INTO b (id, count) VALUES (1, 0)')
    cursor.execute('INSERT OR IGNORE INTO c (id, count) VALUES (1, 0)')
    conn.commit()
    conn.close()

def increment_count(table_name):
    conn = sqlite3.connect('gyeongtaekdb.db')
    cursor = conn.cursor()
    cursor.execute(f'UPDATE {table_name} SET count = count + 1 WHERE id = 1')
    conn.commit()
    cursor.execute(f'SELECT count FROM {table_name} WHERE id = 1')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_counts():
    conn = sqlite3.connect('gyeongtaekdb.db')
    cursor = conn.cursor()
    counts = {}
    for table_name in ['a', 'b', 'c']:
        cursor.execute(f'SELECT count FROM {table_name} WHERE id = 1')
        counts[table_name] = cursor.fetchone()[0]
    conn.close()
    return counts

def reset_counts():
    conn = sqlite3.connect('gyeongtaekdb.db')
    cursor = conn.cursor()
    for table_name in ['a', 'b', 'c']:
        cursor.execute(f'UPDATE {table_name} SET count = 0 WHERE id = 1')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    counts = get_counts()
    response = "오늘의 방문자 수:\n"
    for key, value in counts.items():
        response += f"{key.upper()}: {value} 회 방문\n"
    return response, 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/a')
def route_a():
    count = increment_count('a')
    return f'A 방문자 수: {count}', 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/b')
def route_b():
    count = increment_count('b')
    return f'B 방문자 수: {count}', 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/c')
def route_c():
    count = increment_count('c')
    return f'C 방문자 수: {count}', 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/reset')
def reset():
    reset_counts()
    return "방문자 수를 0으로 초기화 했습니다.", 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080, debug=True)

