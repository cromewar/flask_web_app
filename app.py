from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# info de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user_flask'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'flask_app'
#Conectar con base de datos 
mysql = MySQL(app)

#inicializar sesiones
app.secret_key = 'mysecretkey'

#Ruta principal para Flask
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes')
    data = cur.fetchall()
    return render_template('index.html', clientes = data)

#Otras rutas
@app.route('/add_client', methods=['POST'])
def add_client():
    if request.method == 'POST':
       fullname = request.form['fullname']
       phone = request.form['phone']
       email = request.form['email']
       cur =  mysql.connection.cursor()
       cur.execute('INSERT INTO clientes (fullname, phone, email) VALUES (%s, %s, %s)', (fullname, phone, email))
       mysql.connection.commit()
       flash('Cliente agregado de manera satisfactoria')
       return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_client(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from clientes where id = %s' % id)
    data = cur.fetchall()
    print(data)
    return 'recibido'
    

@app.route('/delete/<string:id>')
def delete_client(id):
   cur = mysql.connection.cursor()
   cur.execute('delete from clientes where id = %s', id)
   mysql.connection.commit()
   flash('Cliente removido de manera exitosa')
   return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3000, debug=True)