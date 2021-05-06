from flask import Blueprint, render_template
from flask import render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from extension import mysql

terapeuta = Blueprint('terapeuta', __name__, static_folder="../static",
                      template_folder="../templates/terapeuta")


@terapeuta.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT terapeuta.*,especialidad.descripcion FROM terapeuta LEFT JOIN especialidad ON especialidad.id_especialidad = terapeuta.id_especialidad')
    data = cur.fetchall()
    cur.execute('SELECT * FROM especialidad')
    espe = cur.fetchall()
    return render_template('terapeuta_home.html', terapeuta=data, especialidad=espe)


@terapeuta.route('/add_therapist', methods=['POST'])
def add_therapist():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        tarifa = request.form['tarifa']
        especialidad = request.form['especialidad']

        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO terapeuta (username, password, email, nombre, apellido, tarifa, id_especialidad) VALUES (%s, %s, %s, %s, %s, %s, %s)', (username, password, email, nombre, apellido, tarifa, especialidad))
        mysql.connection.commit()
        flash('Terapeuta agregado de manera satisfactoria')
        return redirect(url_for('terapeuta.home'))


@terapeuta.route('/edit/<id>')
def get_teraphist(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from terapeuta where id_terapueta = %s' % id)
    data = cur.fetchall()
    cur.execute('SELECT * FROM especialidad')
    espe = cur.fetchall()
    return render_template('edit_terapeuta.html', terapeuta=data[0], especialidad=espe)


@terapeuta.route('/update/<id>', methods=['POST'])
def update_client(id):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        tarifa = request.form['tarifa']
        especialidad = request.form['especialidad']

    cur = mysql.connection.cursor()
    cur.execute("""
                UPDATE terapeuta
                set username = %s, 
                password = %s,
                email = %s,
                nombre = %s,
                apellido = %s,
                tarifa = %s,
                id_especialidad = %s
                where id_terapueta = %s
                """, (username, password, email, nombre, apellido, tarifa, especialidad, id))
    mysql.connection.commit()
    flash('Edición de terapeuta exitosa')
    return redirect(url_for('terapeuta.home'))


@terapeuta.route('/delete/<string:id>')
def delete_therapist(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from terapeuta where id_terapueta = {0}'.format(id))
    mysql.connection.commit()
    flash('Terapeuta removido de manera exitosa')
    return redirect(url_for('terapeuta.home'))
