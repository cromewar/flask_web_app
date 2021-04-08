from flask import Flask

app = Flask(__name__)

#Ruta principal para Flask
@app.route('/')
def Index():
    return 'Hello World'

#Otras rutas
@app.route('/add_client')
def add_client():
    return 'agregar cliente'

@app.route('/edit')
def edit_client():
    return 'edit client'

@app.route('/delete')
def delete_client():
    return 'delete client'

if __name__ == '__main__':
    app.run(port = 3000, debug=True)