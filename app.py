from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from datetime import datetime
import os

# --- CONFIGURACIÓN DE LA APP ---
basedir = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'ventas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

db = SQLAlchemy(app)

# --- MODELOS ---
class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    nota = db.Column(db.Text, nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)

# --- FORMULARIO DE CONTACTO ---
class ContactForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    mensaje = TextAreaField('Mensaje', validators=[DataRequired()])
    enviar = SubmitField('Enviar')

# --- RUTAS ---
@app.route('/')
def index():
    ventas = Venta.query.order_by(Venta.fecha.desc()).all()
    return render_template('index.html', ventas=ventas)

@app.route('/agregar', methods=['POST'])
def agregar():
    cliente = request.form['cliente']
    monto = float(request.form['monto'])
    nota = request.form['nota']
    nueva_venta = Venta(cliente=cliente, monto=monto, nota=nota)
    db.session.add(nueva_venta)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    venta = Venta.query.get_or_404(id)
    db.session.delete(venta)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    form = ContactForm()
    if form.validate_on_submit():
        nuevo_contacto = Contacto(
            nombre=form.nombre.data,
            correo=form.correo.data,
            mensaje=form.mensaje.data
        )
        db.session.add(nuevo_contacto)
        db.session.commit()
        flash("Mensaje enviado correctamente.")
        return redirect(url_for("contacto"))
    return render_template("contact.html", form=form)

# --- EJECUCIÓN ---
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
