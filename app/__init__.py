import psycopg2
import psycopg2.extras
import json

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__,
            static_folder='static/',
            static_url_path='/static',
            template_folder='templates/')
def get_settings():
    with open('settings.json') as f:
        settings = json.load(f)
        return settings
    return None
app.config['settings'] = get_settings()

def get_database():
    settings = app.config['settings']['database']
    conn = psycopg2.connect(database = settings['name'],
                            user     = settings['user'],
                            password = settings['password'],
                            host     = settings['host'],
                            port     = settings['port'])
    return conn

def get_addresses():
    conn = get_database()
    cur = conn.cursor()
    cur.execute('SELECT * FROM endereco')
    data = cur.fetchall()
    conn.commit()
    conn.close()
    return data

@app.route('/')
def index():
    addresses = get_addresses()
    return render_template('index.html', addresses=addresses)
