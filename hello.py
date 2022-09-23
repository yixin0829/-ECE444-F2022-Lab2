from flask import Flask
app = Flask(__name__)
@app.route('/')

def index():
    return '<h1>Hello World!</h1>'

# ex2.2: dynamic routing
@app.route('/user/<name>')
def user(name):
    return f'<h1>Hello, {name}!</h1>'
