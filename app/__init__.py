from flask import Flask, render_template



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/sucursales')
def sucursales():
    return render_template('sucursales.html')

def inicializarApp(config):
    app.config.from_object(config)
    return app
