from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
counter = 1
url_map = {}
host = 'http://localhost:5000/'

@app.route('/', methods=['GET', 'POST'])
def home():
    global counter
    if request.method == 'POST':
        input = request.form
        url = input["url"]
        if url in url_map:
            short_url = url_map[url]
        else:
            short_url = str(encode(counter))
            url_map[url] = short_url
            counter += 1
        return render_template('index.html', short_url=host + short_url)

    return render_template('index.html')


def encode(id):
    base62_characters = "0123456789abcdefghijkhlmnopgrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(base62_characters)
    result = []
    while id > 0:
        val = id % base
        result.append(base62_characters[val])
        id = id // base
    return "".join(result[::-1])


if __name__ == '__main__':
    app.run(debug=True)