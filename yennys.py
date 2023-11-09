from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libros.db'
db = SQLAlchemy(app)

usuarios = {
    'Leandro': {
        'usuario': 'Leandro',
        'password': generate_password_hash('Leandro')
    },
    'Joaco': {
        'usuario': 'Joaco',
        'password': generate_password_hash('Joaco')
    }
}

class Libro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

with app.app_context():
    db.create_all()

    libros = [
        {
            'titulo': 'El Gran Gatsby',
            'autor': 'F. Scott Fitzgerald',
            'precio': 19999,
            'stock': 10
        },
        {
            'titulo': '1984',
            'autor': 'George Orwell',
            'precio': 9999,
            'stock': 14
        },
        {
            'titulo': 'Cien años de soledad',
            'autor': 'Gabriel García Márquez',
            'precio': 11999,
            'stock': 6
        },
        {
            'titulo': 'Matar a un ruiseñor',
            'autor': 'Harper Lee',
            'precio': 9100,
            'stock': 12
        },
        {
            'titulo': 'Don Quijote de la Mancha',
            'autor': 'Miguel de Cervantes',
            'precio': 14000,
            'stock': 10
        },
        {
            'titulo': 'Ulises',
            'autor': 'James Joyce',
            'precio': 7000,
            'stock': 7
        },
        {
            'titulo': 'En busca del tiempo perdido',
            'autor': 'Marcel Proust',
            'precio': 10999,
            'stock': 6
        },
        {
            'titulo': 'Crimen y castigo',
            'autor': 'Fiodor Dostoievski',
            'precio': 8999,
            'stock': 9
        },
        {
            'titulo': 'Orgullo y prejuicio',
            'autor': 'Jane Austen',
            'precio': 4999,
            'stock': 14
        },
        {
            'titulo': 'El señor de los anillos',
            'autor': 'J.R.R. Tolkien',
            'precio': 8999,
            'stock': 2
        }
    ]
    for libro in libros:
        libro_existente = Libro.query.filter_by(titulo=libro['titulo']).first()
        if libro_existente is None:
            nuevo_libro = Libro(titulo=libro['titulo'], autor=libro['autor'], precio=libro['precio'], stock=libro['stock'])
            db.session.add(nuevo_libro)

    db.session.commit()

@app.route('/')
def inicio():
    return '¡Bienvenido a la página de inicio!'

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        if usuario in usuarios:
            flash('El nombre de usuario ya existe. Por favor, elige otro.', 'danger')
        else:
            usuarios[usuario] = {
                'usuario': usuario,
                'password': generate_password_hash(password)
            }
            flash('Registro exitoso', 'success')
            return redirect(url_for('login'))
    return render_template('registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        usuario = usuarios.get(usuario)

        if usuario and check_password_hash(usuario['password'], password):
            session['usuario'] = usuario
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('perfil'))
        else:
            flash('Inicio de sesión fallido. Verifica tus credenciales.', 'danger')

    return render_template('login.html')

@app.route('/libros')
def libros():
    todos_los_libros = Libro.query.all()
    return render_template('libros.html', libros=todos_los_libros)

@app.route('/buscar', methods=['POST'])
def buscar():
    termino_de_busqueda = request.form.get('termino_de_busqueda')
    resultados = Libro.query.filter(
        Libro.titulo.like(f"%{termino_de_busqueda}%") | Libro.autor.like(f"%{termino_de_busqueda}%")
    ).all()
    return render_template('libros.html', libros=resultados)

@app.route('/comprar/<int:libro_id>', methods=['POST'])
def comprar(libro_id):
    libro = Libro.query.get(libro_id)

    if libro:
        if libro.stock > 0:
        
            libro.stock -= 1
            db.session.commit()
            return f'Compraste el libro "{libro.titulo}" por ${libro.precio}'
        else:
            flash('Este libro está agotado', 'danger')
    else:
        flash('Libro no encontrado', 'danger')

    return redirect(url_for('libros'))

@app.route('/perfil')
def perfil():
    usuario = session.get('usuario')
    if usuario:
        return f'¡Bienvenido, {usuario["usuario"]}!'
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)