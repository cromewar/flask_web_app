from flask import Blueprint, render_template
from flask import render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
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
    return render_template('terapia_home.html', terapia=data, terapeuta=terapeuta, cliente=cliente)


@terapia.route('/add_therapy', methods=['POST'])
def add_therapy():
    if request.method == 'POST':
        fecha = request.form['fecha']
        costo = request.form['costo']
        terapeuta = request.form['terapeuta']
        cliente = request.form['cliente']

        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO terapia (fecha, costo, terapeuta_id_terapueta, cliente_id_cliente) VALUES (%s, %s, %s, %s)', (fecha, costo, terapeuta, cliente))
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
        fecha = request.form['fecha']
        costo = request.form['costo']
        terapeuta = request.form['terapeuta']
        cliente = request.form['cliente']

    cur = mysql.connection.cursor()
    cur.execute("""
                UPDATE terapia
                set fecha = %s, 
                costo = %s,
                terapeuta_id_terapueta = %s,
                cliente_id_cliente = %s
                where id_terapia = %s
                """, (fecha, costo, terapeuta, cliente, id))
    mysql.connection.commit()
    flash('Edición de terapia exitosa')
    return redirect(url_for('terapia.home'))


@terapia.route('/delete/<string:id>')
def delete_therapy(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from terapia where id_terapia = {0}'.format(id))
    mysql.connection.commit()
    flash('Terapia removida de manera exitosa')
    return redirect(url_for('terapia.home'))
