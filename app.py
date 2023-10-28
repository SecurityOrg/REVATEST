import os
import pickle
import base64
from flask import Flask, request

app = Flask(__name__)

app.secret_key = 'secret'

users = {'admin': 'password123'}

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username in users and users[username] == password:
        token = base64.b64encode(os.urandom(5)).decode('utf-8')
        return f"Logged in! Your session token is {token}"
    else:
        return "Invalid credentials!", 401

@app.route('/echo', methods=['POST'])
def echo():
    user_input = request.form.get('input')
    result = os.popen(user_input).read()
    return result

@app.route('/pickle', methods=['POST'])
def load_pickle():
    data = base64.b64decode(request.form.get('data'))
    obj = pickle.loads(data)
    return str(obj)

@app.route('/redirect')
def redirect():
    url = request.args.get('url')
    return flask.redirect(url)

@app.route('/eval', methods=['POST'])
def evaluate():
    code = request.form.get('code')
    return str(eval(code))

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    comment = request.args.get('comment', '')
    return f"<html><body>Last comment: {comment}</body></html>"

@app.route('/readfile')
def read_file():
    filename = request.args.get('filename')
    with open(filename, 'r') as file:
        content = file.read()
    return content

if __name__ == '__main__':
    app.run(debug=True)
