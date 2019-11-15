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
    cur.execute('''
    SELECT
        q.id_quarto,
        q.nu_quarto,
        t.tipo
    FROM quarto AS q
    INNER JOIN tipo_quarto AS t ON t.id_tipo = q.id_tipo_quarto;
     ''')
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

def set_tipo_quarto(novo_tipo_quarto):
    conn = get_database()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tipo_quarto WHERE tipo = '"+novo_tipo_quarto+"'")
    data = cur.fetchall()
    if (not data):
        qry = "INSERT INTO tipo_quarto (tipo) VALUES('"+novo_tipo_quarto+"')"
        cur.execute(qry)
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
                                         precos_temporada=precos_temporada,
                                         tipos_quarto=tipos_quarto,
                                         hoteis=hoteis)

@app.route('/tipoquarto', methods=['GET', 'POST'])
def tipo_quarto():
    resp = False
    if request.method == 'POST':
        novo_tipo_quarto = request.form['tipo_quarto']
        print('[tipoquarto] Request insert on database: ', novo_tipo_quarto)
        resp = True if set_tipo_quarto(novo_tipo_quarto) else False
        print('[tipoquarto] Insert response: ', resp)

    tipos_quarto = get_tipo_quarto()
    return render_template('tipoquarto.html', tipos_quarto=tipos_quarto, mostra_aviso=resp)

@app.route('/preco_temporada', methods=['GET', 'POST'])
def preco_temporada():
    msg = ""
    work = True
    if request.method == 'POST':
        value_preco_temporada = request.form['preco_temporada']
        value_nome_temporada = request.form['nome_temporada']
        print(value_preco_temporada)
        print(value_nome_temporada)
        conn = get_database()
        cur = conn.cursor()
        query = "INSERT INTO preco_temporada (nu_preco_diaria, nome_temporada) VALUES("+value_preco_temporada+", '"+value_nome_temporada+"')"
        try:
            cur.execute(query)
            conn.commit()
            print("Executed:"+query)
            work = True
        
        except:
            msg = "Fail executing the query"
            work = False

    
    else:
        work = False

    precos_temporada = get_preco_temporada()
    return render_template('preco_temporada.html', precos_temporada=precos_temporada, work=work, msg=msg)

@app.route('/preco_temporada/<id_preco_temporada>')
def remove_temporada(id_preco_temporada):

    conn = get_database()
    cur = conn.cursor()
    query = "DELETE FROM preco_temporada WHERE id_preco_temporada = "+id_preco_temporada
    msg = ""
    work = True

    try:
        cur.execute(query)
        conn.commit()
        msg = "Remoção Efetuada"
        print("Executed:"+query)
        work = True

    except:
        msg = "Não foi possível remover a temporada, esta pode estar em uso ou nao existir."
        print(msg)
        work = False

    precos_temporada = get_preco_temporada()
    return render_template('preco_temporada.html', precos_temporada=precos_temporada, msg=msg, work=work)

@app.route('/preco_temporada/update_temporada', methods=['GET', 'POST'])
def update_temporada():
    msg = ""
    work = True
    if request.method == 'POST':
        id_preco_temporada = request.form['id_preco_temporada']
        value_preco_temporada = request.form['preco_temporada']
        value_nome_temporada = request.form['nome_temporada']
        print(value_preco_temporada)
        print(value_nome_temporada)
        conn = get_database()
        cur = conn.cursor()
        query = "UPDATE preco_temporada SET nu_preco_diaria = "+value_preco_temporada+", nome_preco_temporada = "+value_nome_temporada+" WHERE id_preco_temporada = "+id_preco_temporada
        
        try:
            cur.execute(query)
            conn.commit()
            print("Executed:"+query)
            work = True
        
        except:
            msg = "Fail executing the query"
            work = False

    else:
        work = False

    precos_temporada = get_preco_temporada()
    return render_template('preco_temporada.html', precos_temporada=precos_temporada)

@app.route('/quarto', methods=['GET', 'POST'])
def quarto():
    if request.method == 'POST':
        tipo_quarto = request.form['tipo_quarto']
        numero_quarto = request.form['numero_quarto']
        conn = get_database()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO quarto (id_hotel, id_tipo_quarto, nu_quarto)
            VALUES (1, {}, {})
        '''.format(tipo_quarto, numero_quarto))
        conn.commit()
        conn.close()
    quartos = get_quartos()
    tipos = get_tipo_quarto()
    return render_template('quarto.html', quartos=quartos, tipos=tipos)

    return render_template('preco_temporada.html', precos_temporada=precos_temporada, work=work, msg=msg)
