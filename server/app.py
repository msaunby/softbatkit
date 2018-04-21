# softbatkit-app.py
from bottle import run, route, get, post, request
from tuner import tuner_top_block

tb = None

@route('/')
def home():
    return "<h1>SoftBatKit</h1>"

@route('/about')
def about():
    return "Softbatkit web control app."

@get('/freq')
def freq():
    data = {}
    data['f'] = 1
    return """
<form action="/freq" method="post">
  <input type="text" name="f" />
  <input type="submit" value="submit" />
</form>"""

@post('/freq')
def do_freq():
    global tb
    f = request.forms.get('f')
    data = {}
    data['f'] = f
    tb.set_freq( float(f) )

    return data



if __name__ == '__main__':
    loop_in = "hw:Loopback,0,0"  # The other side of this device is hw:Loopback,1,0
    loop_out = "hw:Loopback,1,1" # The other side of this device is hw:Loopback,0,1
    global tb
    tb = tuner_top_block( loop_in, 96000, loop_out, 48000, 50000, 1.0)
    tb.start()
    run(host='localhost', port=8080, debug=True)
