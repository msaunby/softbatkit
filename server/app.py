# softbatkit-app.py
from bottle import run, route, get, post, request

@route('/')
def home():
    return "<h1>SoftBatKit</h1>"

@route('/about')
def about():
    return "Softbatkit web control app."

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
