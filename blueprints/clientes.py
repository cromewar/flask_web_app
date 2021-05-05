from flask import Blueprint, render_template
from flask import render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from extension import mysql

client = Blueprint('client', __name__,
                   static_folder="../static", template_folder="../templates")


@client.route('/')
def home():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM cliente')
        data = cur.fetchall()
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'], cliente=data)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@client.route('/add_client', methods=['POST'])
def add_client():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nombres = request.form['nombres']
        email = request.form['email']
        cedula = request.form['cedula']

        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO cliente (username, nombres, password, email, cedula) VALUES (%s, %s, %s, %s, %s)', (username, nombres, password, email, cedula))
        mysql.connection.commit()
        flash('Cliente agregado de manera satisfactoria')
        return redirect(url_for('client.home'))


@client.route('/edit/<id>')
def get_client(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from cliente where id_cliente = %s' % id)
    data = cur.fetchall()
    return render_template('edit_client.html', cliente=data[0])


@client.route('/update/<id>', methods=['POST'])
def update_client(id):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nombres = request.form['nombres']
        email = request.form['email']
        cedula = request.form['cedula']

    cur = mysql.connection.cursor()
    cur.execute("""
                UPDATE cliente
                set username = %s, 
                nombres = %s,
                password = %s,
                email = %s,
                cedula = %s
                where id_cliente = %s
                """, (username, nombres, password, email, cedula, id))
    mysql.connection.commit()
    flash('Edición de cliente exitosa')
    return redirect(url_for('client.home'))


@client.route('/delete/<string:id>')
def delete_client(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from cliente where id_cliente = {0}'.format(id))
    mysql.connection.commit()
    flash('Cliente removido de manera exitosa')
    return redirect(url_for('client.home'))
