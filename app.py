from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ventas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    nota = db.Column(db.Text, nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
