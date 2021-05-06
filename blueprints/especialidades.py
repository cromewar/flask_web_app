from flask import Blueprint, render_template
from flask import render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from extension import mysql

especialidad = Blueprint('especialidad', __name__,
                         template_folder="../templates/especialidad", static_folder="../static")


@especialidad.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM especialidad')
    espe = cur.fetchall()
    return render_template('especialidad_home.html', especialidad=espe)


@especialidad.route('/create_new', methods=['POST'])
def create_new():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        item_uno = request.form['item_uno']
        item_dos = request.form['item_dos']
        item_tres = request.form['item_tres']

        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO especialidad (descripcion, item_uno, item_dos, item_tres) VALUES (%s, %s, %s, %s)', (descripcion, item_uno, item_dos, item_tres))
        mysql.connection.commit()
        flash('especialidad agregado de manera satisfactoria')
        return redirect(url_for('especialidad.home'))


@especialidad.route('/edit/<id>')
def get_especialidad(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from especialidad where id_especialidad = %s' % id)
    data = cur.fetchall()
    return render_template('edit_especialidad.html', especialidad=data[0])


@especialidad.route('/update/<id>', methods=['POST'])
def update_client(id):
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        item_uno = request.form['item_uno']
        item_dos = request.form['item_dos']
        item_tres = request.form['item_tres']

    cur = mysql.connection.cursor()
    cur.execute("""
                UPDATE especialidad
                set descripcion = %s, 
                item_uno = %s,
                item_dos = %s,
                item_tres = %s
                where id_especialidad = %s
                """, (descripcion, item_uno, item_dos, item_tres, id))
    mysql.connection.commit()
    flash('Edición de Especialidad exitosa')
    return redirect(url_for('especialidad.home'))


@especialidad.route('/delete/<string:id>')
def delete_client(id):
    cur = mysql.connection.cursor()
    cur.execute(
        'delete from especialidad where id_especialidad = {0}'.format(id))
    mysql.connection.commit()
    flash('Especialidad removida de manera exitosa')
    return redirect(url_for('especialidad.home'))
