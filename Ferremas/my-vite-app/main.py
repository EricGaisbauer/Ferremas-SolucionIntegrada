from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Usamos SQLite para simplificar
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Despacho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto = db.Column(db.String(70), unique=True)
    proceso = db.Column(db.String(100))

    def __init__(self, producto, proceso):
        self.producto = producto
        self.proceso = proceso

class DespachoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Despacho

despacho_schema = DespachoSchema()
despachos_schema = DespachoSchema(many=True)

@app.route('/task', methods=['POST'])
def create_task():
    producto = request.json['producto']
    proceso = request.json['proceso']
    new_task = Despacho(producto, proceso)
    db.session.add(new_task)
    db.session.commit()
    return despacho_schema.jsonify(new_task)

@app.route('/task', methods=['GET'])
def get_tasks():
    all_tasks = Despacho.query.all()
    result = despachos_schema.dump(all_tasks)
    return jsonify(result)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
