from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# Definir la ruta en donde se encuentran los templates
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

# Crea una instancia de la aplicación Flask
app = Flask(__name__, template_folder=template_dir)

# Configuración para establecer la conexión
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres.yltrcinrscjjmkwhanht:ejemplo.123@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Definir instancia SQLAlchemy para definir la conexión a la bdd
bdd = SQLAlchemy(app)

# Definir el modelo de la base de datos
class Usuario(bdd.Model):
    id = bdd.Column(bdd.Integer, primary_key=True)
    nombre = bdd.Column(bdd.String(50), nullable=False)
    apellido = bdd.Column(bdd.String(50), nullable=False)
    email = bdd.Column(bdd.String(120), unique=True, nullable=False)

# Crear las tablas en la base de datos
with app.app_context():
    bdd.create_all()

# Definir la ruta principal de la aplicación
@app.route('/', methods=['GET'])
def home():
    usuarios = Usuario.query.all()
    #usuarios = Usuario.query.filter(Usuario.nombre == "Juan")
    return render_template('index.html', usuarios=usuarios)

@app.route('/add', methods=['POST'])
def add_user():
    if not request.is_json:
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
    else:
        nombre = request.json.get('nombre')
        apellido = request.json.get('apellido')
        email = request.json.get('email')
        
    nuevo_usuario = Usuario(nombre=nombre, apellido=apellido, email=email)
    bdd.session.add(nuevo_usuario)
    bdd.session.commit()
    return redirect(url_for('home'))
    
# Ruta para eliminar un usuario
@app.route('/delete/<int:id>')
def delete(id):
    usuario = Usuario.query.get_or_404(id)
    bdd.session.delete(usuario)
    bdd.session.commit()
    return redirect(url_for('home'))

# Ruta para editar un usuario
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuario.nombre = request.form['nombre']
        usuario.apellido = request.form['apellido']
        usuario.email = request.form['email']

        bdd.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', usuario=usuario)

if __name__ == '__main__':
    app.run(debug=True, port=4000)
