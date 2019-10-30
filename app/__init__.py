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

def get_quartos():
    conn = get_database()
    cur = conn.cursor()
    cur.execute('SELECT * FROM quarto')
    data = cur.fetchall()
    conn.commit()
    conn.close()
    return data

def get_preco_temporada():
    conn = get_database()
    cur = conn.cursor()
    cur.execute('SELECT * FROM preco_temporada')
    data = cur.fetchall()
    conn.commit()
    conn.close()
    return data

def get_hoteis():
    conn = get_database()
    cur = conn.cursor()
    cur.execute('SELECT * FROM hotel')
    data = cur.fetchall()
    conn.commit()
    conn.close()
    return data

def get_tipo_quarto():
    conn = get_database()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tipo_quarto')
    data = cur.fetchall()
    conn.commit()
    conn.close()
    return data

@app.route('/')
def index():
    quartos = get_quartos()
    precos_temporada = get_preco_temporada()
    tipos_quarto = get_tipo_quarto()
    hoteis = get_hoteis()
    return render_template('index.html', quartos=quartos, 
        precos_temporada=precos_temporada, tipos_quarto=tipos_quarto, hoteis=hoteis)

