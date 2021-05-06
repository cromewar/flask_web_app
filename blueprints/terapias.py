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
    return render_template('terapeuta_home.html', terapia=data, terapeuta=data, cliente=cliente)
