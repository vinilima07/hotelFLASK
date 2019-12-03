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

def update_quarto(id_quarto, tipo_quarto, numero_quarto, id_hotel):
    conn = get_database()
    cur = conn.cursor()
    cur.execute('''
    UPDATE quarto SET
        id_hotel = {},
        id_tipo_quarto = {},
        nu_quarto = {}
    WHERE id_quarto = {};
     '''.format(id_hotel, tipo_quarto, numero_quarto, id_quarto))
    conn.commit()
    conn.close()

def get_quarto_by_id(id_quarto, quartos):
    for quarto in quartos:
        if int(quarto[0]) == int(id_quarto):
            return quarto

def get_temporada_by_id(id_temporada, temporadas):
    for temporada in temporadas:
        if int(temporada[0]) == int(id_temporada):
            return temporada

def get_quartos_by_cidade(cidade):
    conn = get_database()
    cur = conn.cursor()
    cur.execute('''
    SELECT
        q.id_quarto,
        q.nu_quarto,
        t.tipo,
        h.nome_hotel,
        h.cidade
    FROM quarto AS q
    INNER JOIN tipo_quarto AS t ON t.id_tipo = q.id_tipo_quarto
    INNER JOIN hotel AS h ON h.id_hotel = q.id_hotel
    WHERE h.cidade = '{}';
     '''.format(cidade))
    data = cur.fetchall()
    conn.commit()
    conn.close()
    return data

def get_quartos():
    conn = get_database()
    cur = conn.cursor()
    cur.execute('''
    SELECT
        q.id_quarto,
        q.nu_quarto,
        t.tipo,
        h.nome_hotel
    FROM quarto AS q
    INNER JOIN tipo_quarto AS t ON t.id_tipo = q.id_tipo_quarto
    INNER JOIN hotel AS h ON h.id_hotel = q.id_hotel;
     ''')
    data = cur.fetchall()
    conn.commit()
    conn.close()
    return data

def delete_quarto(id_quarto):
    conn = get_database()
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM quarto WHERE id_quarto = {}
    '''.format(id_quarto))
    conn.commit()
    conn.close()

def delete_tipo(id_tipo):
    conn = get_database()
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM tipo_quarto WHERE id_tipo = {}
    '''.format(id_tipo))
    conn.commit()
    conn.close()

def delete_preco_temporada(id_preco_temporada):
    msg = ""
    conn = get_database()
    cur = conn.cursor()
    try:
        cur.execute('''
            DELETE FROM preco_temporada WHERE id_preco_temporada = {}
        '''.format(id_preco_temporada))
        conn.commit()
    except:
        msg = "Fail executing the query"
        work = False
    conn.close()
    return msg

def insert_quarto(id_hotel, tipo_quarto, numero_quarto):
    conn = get_database()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO quarto (id_hotel, id_tipo_quarto, nu_quarto)
        VALUES ({},{},{})
    '''.format(id_hotel, tipo_quarto, numero_quarto))
    conn.commit()
    conn.close()

def insert_preco_temporada(preco, nome_temporada):
    conn = get_database()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO preco_temporada (nu_preco_diaria, nome_temporada)
        VALUES ({},'{}')
    '''.format(preco, nome_temporada))
    conn.commit()
    conn.close()

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

def get_tipo_by_id(id_tipo, tipos):
    for tipo in tipos:
        if int(tipo[0]) == int(id_tipo):
            return tipo

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

def update_preco_temporada(request_id, preco_temporada, nome_temporada):
    conn = get_database()
    cur = conn.cursor()
    cur.execute("SELECT * FROM preco_temporada WHERE nu_preco_diaria = {} AND nome_temporada = '{}'".format(preco_temporada, nome_temporada))
    data = cur.fetchall()
    if (not data):
        qry = "UPDATE preco_temporada SET nu_preco_diaria = {}, nome_temporada = '{}' WHERE id_preco_temporada = {}".format(preco_temporada, nome_temporada, request_id)
        cur.execute(qry)
    conn.commit()
    conn.close()
    return data

def insert_preco_temporada(preco, nome_temporada):
    conn = get_database()
    cur = conn.cursor()
    cur.execute("SELECT * FROM preco_temporada WHERE nu_preco_diaria = {} AND nome_temporada = '{}'".format(preco, nome_temporada))
    data = cur.fetchall()
    if (not data):
        cur.execute('''
            INSERT INTO preco_temporada (nu_preco_diaria, nome_temporada)
            VALUES ({},'{}')
        '''.format(preco, nome_temporada))
    conn.commit()
    conn.close()
    return data

def update_tipo_quarto(id_tipo_quarto, tipo_quarto):
    conn = get_database()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tipo_quarto WHERE tipo = '{}'".format(tipo_quarto))
    data = cur.fetchall()
    if (not data):
        qry = "UPDATE tipo_quarto SET tipo = '{}' WHERE id_tipo = {}".format(tipo_quarto, id_tipo_quarto)
        cur.execute(qry)
    conn.commit()
    conn.close()
    return data

def insere_reserva(id_quarto, dt_inicio, dt_fim):
    conn = get_database()
    cur = conn.cursor()
    conn.commit()
    conn.close()

def reserva_pacote(quarto, dt_inicio, dt_fim):
    conn = get_database()
    cur = conn.cursor()
    cur.execute("SELECT * FROM reserva_hotel WHERE id_quarto_quarto = {} AND dt_inicio >= '{}' AND dt_fim <= '{}'".format(quarto, dt_inicio, dt_fim))
    data = cur.fetchall() # Verifica se reserva disponível.

    if data is not None:
        cur.execute("INSERT INTO reserva_hotel (id_quarto_quarto, dt_inicio, dt_fim) VALUES ({}, '{}', '{}') RETURNING id_reserva_quarto;".format(quarto, dt_inicio, dt_fim))
        id_reserva_quarto = cur.fetchall()

        # Reserva carro, simulação.
        import random
        id_reserva_carro = random.randint(0, 50)

        cur.execute("INSERT INTO reserva_pacote (id_reserva_hotel_reserva_hotel, id_reserva_carro) VALUES ({}, {})".format(id_reserva_quarto[0][0], id_reserva_carro))

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
        resp = True if set_tipo_quarto(novo_tipo_quarto) else False

    deleteID = request.args.get('delete')
    if deleteID is not None:
        delete_tipo(deleteID)
        return redirect(url_for('tipo_quarto'))

    tipos_quarto = get_tipo_quarto()
    return render_template('tipoquarto.html', tipos_quarto=tipos_quarto, mostra_aviso=resp)

@app.route('/preco_temporada', methods=['GET', 'POST'])
def preco_temporada():
    resp = False
    msg = ""
    if request.method == 'POST':
        value_preco_temporada = request.form['preco_temporada']
        value_nome_temporada = request.form['nome_temporada']
        resp = True if insert_preco_temporada(value_preco_temporada, value_nome_temporada) else False

    precos_temporada = get_preco_temporada()
    deleteID = request.args.get('delete')
    if deleteID is not None:
        msg = delete_preco_temporada(deleteID)
        return render_template('preco_temporada.html', precos_temporada=precos_temporada, mostra_aviso=resp, msg=msg)
    return render_template('preco_temporada.html', precos_temporada=precos_temporada, mostra_aviso=resp, msg=msg)

@app.route('/quarto', methods=['GET', 'POST'])
def quarto():
    if request.method == 'POST':
        tipo_quarto = request.form['tipo_quarto']
        numero_quarto = request.form['numero_quarto']
        id_hotel = request.form['id_hotel']
        insert_quarto(id_hotel, tipo_quarto, numero_quarto)

    deleteID = request.args.get('delete')
    if deleteID is not None:
        delete_quarto(deleteID)
        return redirect(url_for('quarto'))

    quartos = get_quartos()
    tipos = get_tipo_quarto()
    hoteis = get_hoteis()
    return render_template('quarto.html', quartos=quartos, tipos=tipos, hoteis=hoteis)

@app.route('/update', methods=['GET', 'POST'])
def update():
    tipo = request.args.get('type')
    request_id = request.args.get('update')

    if request.method == 'POST':
         if tipo == "1":
            tipo_quarto = request.form['tipo_quarto']
            resp = True if update_tipo_quarto(request_id, tipo_quarto) else False
            tipos_quarto = get_tipo_quarto()
            return render_template('tipoquarto.html', tipos_quarto=tipos_quarto, mostra_aviso=resp)

         if tipo == "2":
            tipo_quarto = request.form['tipo_quarto']
            numero_quarto = request.form['numero_quarto']
            id_hotel = request.form['id_hotel']
            update_quarto(request_id, tipo_quarto, numero_quarto, id_hotel)
            return redirect(url_for('quarto'))

         if tipo == "3":
            preco_temporada = request.form['preco_temporada']
            nome_temporada = request.form['nome_temporada']
            resp = True if update_preco_temporada(request_id, preco_temporada, nome_temporada) else False
            precos_temporada=get_preco_temporada()
            return render_template('preco_temporada.html', precos_temporada=precos_temporada, mostra_aviso=resp)

    if tipo == "1":
        tipos = get_tipo_quarto()
        tipo_quarto = get_tipo_by_id(request_id, tipos)
        return render_template('update.html', tipo_quarto=tipo_quarto, op=tipo)
    if tipo == "2":
        quartos = get_quartos()
        quarto = get_quarto_by_id(request_id, quartos)
        tipos = get_tipo_quarto()
        hoteis = get_hoteis()
        return render_template('update.html', quartos=quartos, tipos=tipos, hoteis=hoteis, quarto=quarto, op=tipo)
    if tipo == "3":
        precos = get_preco_temporada()
        temporada = get_temporada_by_id(request_id, precos)
        return render_template('update.html', temporada=temporada, op=tipo)

@app.route('/reserva_quarto', methods=['GET', 'POST'])
def reserva_quarto():
    quartos = get_quartos()
    if request.method == 'POST':
        id_quarto = request.form['id_quarto']
        dt_inicio = request.form['dt_inicio']
        dt_fim = request.form['dt_fim']
        insere_reserva(id_quarto, dt_inicio, dt_fim)

    cidade = request.args.get('cidade')
    if cidade is not None:
        quartos = get_quartos_by_cidade(cidade)
    else:
        quartos = get_quartos()

    return render_template('reserva_quarto.html', quartos=quartos)

@app.route('/reserva_pacote', methods=['GET', 'POST'])
def reserva_pacote():
    quartos = get_quartos()
    resp = False
    if request.method == 'POST':
        id_quarto = request.form['id_quarto']
        dt_inicio = request.form['dt_inicio']
        dt_fim = request.form['dt_fim']
        print(dt_inicio)

        err = reserva_pacote(id_quarto, dt_inicio, dt_fim)
        if err:
            resp = True

    filtro = request.args.get('filtrar')
    if filtro is not None:
        pass

    return render_template('reserva_pacote.html', quartos=quartos, mostra_aviso=resp)
