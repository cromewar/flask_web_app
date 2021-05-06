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
