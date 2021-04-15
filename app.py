from flask import Flask, request, render_template, redirect
from flask_cors import CORS
import sqlite3
from sqlite3 import OperationalError

app = Flask(__name__)
CORS(app)
counter = 1
host = 'http://localhost:8080/'

def init():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Create table - URL_MAP
    try:
        c.execute('''CREATE TABLE URL_MAP
                 ([ID] INTEGER PRIMARY KEY AUTOINCREMENT,[URL] text NOT NULL, [SHORT_URL] text NOT NULL, [COUNTER] INTEGER NOT NULL)''')
    except OperationalError:
        pass
    conn.commit()

@app.route('/create_short_url', methods=['GET', 'POST'])
def home():
    global counter
    if request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/json':
            input = request.get_json()
        else:
            input = request.form

        url = input["url"]
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            res = cursor.execute(
                'SELECT SHORT_URL FROM URL_MAP WHERE URL LIKE ?', (url,))
            short = res.fetchone()

            if short is not None:
                short_url = short[0]
            else:
                cursor.execute('SELECT COUNT(*) from URL_MAP')
                cur_result = cursor.fetchone()
                if cur_result[0] == 0:
                    counter = 0
                else:
                    cursor.execute('SELECT MAX(COUNTER) from URL_MAP')
                    counter = cursor.fetchone()[0]
                print("counter is ", counter)
                short_url = str(encode(counter + 1))
                res = cursor.execute(
                    'INSERT INTO URL_MAP (URL, SHORT_URL, COUNTER) VALUES (?,?,?)', (url, short_url, counter+1)
                )
            conn.commit()
            return render_template('index.html', short_url=host+str("short_url/") + str(short_url))

    return render_template('index.html')

@app.route('/short_url/<short_url>')
def redirect_short_url(short_url):
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            res = cursor.execute('SELECT URL FROM URL_MAP WHERE SHORT_URL LIKE ?', (short_url,))
            try:
                original_url = res.fetchone()
                if original_url is not None:
                    return redirect(original_url[0])
            except Exception as e:
                print(e)
        return redirect(host+str("create_short_url"))

    except OverflowError as e:
        print(str(e))

def encode(id):
    base62_characters = "0123456789abcdefghijkhlmnopgrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = 62
    result = []
    while id > 0:
        val = id % base
        result.append(base62_characters[val])
        id = id // base
    return "".join(result[::-1])


if __name__ == '__main__':
    init()
    app.run(host ='0.0.0.0', port = 8080, debug = True)
    #app.run(debug=True)
