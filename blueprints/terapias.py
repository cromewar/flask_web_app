from controller.terapy_check import check_conflict
from datetime import datetime
from flask import Blueprint, render_template
from flask import render_template, request, redirect, url_for, session, flash, jsonify, json
from flask_mysqldb import MySQL
import flask
import MySQLdb.cursors
import re
from extension import mysql


terapia = Blueprint('terapia', __name__, static_folder="../static",
                    template_folder="../templates/terapia")


@terapia.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT terapia.*,terapeuta.nombre,cliente.nombres FROM terapia LEFT JOIN terapeuta ON terapeuta.id_terapueta = terapia.terapeuta_id_terapueta LEFT JOIN cliente ON cliente.id_cliente = terapia.cliente_id_cliente')
    data = cur.fetchall()


    cur.execute('SELECT * FROM cliente')
    cliente = cur.fetchall()
    cur.execute('SELECT * FROM terapeuta')
    terapeuta = cur.fetchall()
    cur.execute('SELECT * FROM especialidad')
    especialidades = cur.fetchall()

    return render_template('terapia_home.html', terapia=data, terapeuta=terapeuta, cliente=cliente, especialidades = especialidades)


@terapia.route('/factura/<id>')
def factura(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM terapia WHERE id_terapia  = %s' % id)
    data = cur.fetchall()

    return render_template('terapia_factura.html', terapia=data[0])

@terapia.route('/livesearch', methods=["POST","GET"])
def livesearch():
    searchbox = request.form.get('text')
    cur = mysql.connection.cursor()
    query = "SELECT terapia.*,terapeuta.nombre,cliente.nombres, especialidad.descripcion FROM terapia LEFT JOIN terapeuta ON terapeuta.id_terapueta = terapia.terapeuta_id_terapueta LEFT JOIN cliente ON cliente.id_cliente = terapia.cliente_id_cliente LEFT JOIN especialidad ON especialidad.id_especialidad = terapeuta.id_especialidad WHERE especialidad.descripcion LIKE '{}%'  OR terapeuta.nombre LIKE '{}%' OR cliente.nombres LIKE '{}%' ".format(searchbox, searchbox, searchbox)
    cur.execute(query)
    row_headers =[x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)

@terapia.route('/livesearch2', methods=["POST","GET"])
def livesearch2():
    date = request.form.get('date')
    esp1 = request.form.get('especialidad1')
    esp2 = request.form.get('especialidad2')
    cur = mysql.connection.cursor()
    query = "SELECT terapia.*,terapeuta.nombre,cliente.nombres, especialidad.descripcion FROM terapia LEFT JOIN terapeuta ON terapeuta.id_terapueta = terapia.terapeuta_id_terapueta LEFT JOIN cliente ON cliente.id_cliente = terapia.cliente_id_cliente LEFT JOIN especialidad ON especialidad.id_especialidad = terapeuta.id_especialidad WHERE date(fecha) = '{}' and ( especialidad.descripcion = '{}' or especialidad.descripcion = '{}')".format(date, esp1, esp2)
    cur.execute(query)
    row_headers =[x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)



    


@terapia.route('/add_therapy', methods=['POST'])
def add_therapy():
    if request.method == 'POST':
        

        cliente = request.form['cliente']
        terapeuta = request.form['terapeuta']
        fecha = request.form['fecha']
        duracion = request.form['duracion']
        fin = request.form['fin']
        costo = request.form['costo']
        fecha_ini, hour_ini = (str(i) for i in fecha.split('T'))
        h1, m1 = (int(i) for i in hour_ini.split(':'))

        cur = mysql.connection.cursor()
        cur.execute(
        'SELECT terapia.*,terapeuta.nombre,cliente.nombres FROM terapia LEFT JOIN terapeuta ON terapeuta.id_terapueta = terapia.terapeuta_id_terapueta LEFT JOIN cliente ON cliente.id_cliente = terapia.cliente_id_cliente')
        data = cur.fetchall()

       
        
        print(check_conflict(data, fecha_ini, h1, cliente, terapeuta))
        if check_conflict(data, fecha_ini, h1, cliente, terapeuta):
            flash('La Terapia no se pudo agregar debido a conflicto con fecha y hora')
            return redirect(url_for('terapia.home'))
        else:
            cur.execute(
                'INSERT INTO terapia (cliente_id_cliente, terapeuta_id_terapueta, fecha, duracion, fin, costo) VALUES (%s, %s, %s, %s, %s, %s)', (cliente, terapeuta, fecha, duracion, fin, costo))
            mysql.connection.commit()
            flash('Terapia agregada de manera satisfactoria')
            return redirect(url_for('terapia.home'))


@terapia.route('/edit/<id>')
def get_terapy(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM terapia WHERE id_terapia  = %s' % id)
    data = cur.fetchall()
    cur.execute('SELECT * FROM cliente')
    cliente = cur.fetchall()
    cur.execute('SELECT * FROM terapeuta')
    terapeuta = cur.fetchall()
    return render_template('edit_terapia.html', terapia=data[0], terapeuta=terapeuta, cliente=cliente)


@terapia.route('/update/<id>', methods=['POST'])
def update_client(id):
    if request.method == 'POST':
        cliente = request.form['cliente']
        terapeuta = request.form['terapeuta']
        fecha = request.form['fecha']
        duracion = request.form['duracion']
        fin = request.form['fin']
        costo = request.form['costo']
        fecha_ini, hour_ini = (str(i) for i in fecha.split('T'))
        h1, m1 = (int(i) for i in hour_ini.split(':'))

        cur = mysql.connection.cursor()
        cur.execute(
        'SELECT terapia.*,terapeuta.nombre,cliente.nombres FROM terapia LEFT JOIN terapeuta ON terapeuta.id_terapueta = terapia.terapeuta_id_terapueta LEFT JOIN cliente ON cliente.id_cliente = terapia.cliente_id_cliente')
        data = cur.fetchall()
        
        if check_conflict(data, fecha_ini, h1, cliente, terapeuta):
            flash('La Terapia no se pudo agregar debido a conflicto con fecha y hora')
            return redirect(url_for('terapia.home'))
        else:
            cur = mysql.connection.cursor()
            cur.execute("""
                        UPDATE terapia
                        set cliente_id_cliente = %s,
                        terapeuta_id_terapueta = %s,
                        fecha = %s, 
                        duracion = %s,
                        fin = %s,
                        costo = %s
                        where id_terapia = %s
                        """, (cliente,terapeuta,fecha,duracion,fin, costo, id))
            mysql.connection.commit()
            flash('Edici??n de terapia exitosa')
            return redirect(url_for('terapia.home'))


@terapia.route('/delete/<string:id>')
def delete_therapy(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from terapia where id_terapia = {0}'.format(id))
    mysql.connection.commit()
    flash('Terapia removida de manera exitosa')
    return redirect(url_for('terapia.home'))
