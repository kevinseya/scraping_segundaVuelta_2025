from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    path = r'D:\scraping\web_scraping\static\data.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
