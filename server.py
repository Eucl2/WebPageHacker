from flask import Flask, request
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app) #cors

def init_db():
    with sqlite3.connect('user_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                browser TEXT,
                platform TEXT,
                language TEXT,
                online_status TEXT,
                time_on_page REAL,
                mouse_moves TEXT
            )
        ''')
        conn.commit()

@app.route('/collect_data', methods=['POST', 'OPTIONS'])
def collect_data():
    if request.method == 'OPTIONS': # Important as the options request wasn't allowing to see the data
        return '', 200
    
    data = request.json
    
    browser_info = data.get('browser', 'Unknown')
    platform = data.get('platform', 'Unknown')
    language = data.get('language', 'Unknown')
    online_status = data.get('online', 'Unknown')
    time_on_page = data.get('timeOnPage', 0)
    mouse_moves = json.dumps(data.get('mouseMoves', []))

    with sqlite3.connect('user_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_data (browser, platform, language, online_status, time_on_page, mouse_moves)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (browser_info, platform, language, online_status, time_on_page, mouse_moves))
        conn.commit()

    print("--- Data Stored in Database ---")
    return "Data received!", 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
