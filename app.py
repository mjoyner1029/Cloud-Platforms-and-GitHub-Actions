# app.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Sum model
class Sum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a = db.Column(db.Integer, nullable=False)
    b = db.Column(db.Integer, nullable=False)
    result = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Sum {self.id}: {self.a} + {self.b} = {self.result}>'

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/sum', methods=['POST'])
def add_sum():
    data = request.json
    a = data.get('a')
    b = data.get('b')
    result = a + b
    new_sum = Sum(a=a, b=b, result=result)
    db.session.add(new_sum)
    db.session.commit()
    return jsonify({"id": new_sum.id, "a": a, "b": b, "result": result}), 201

@app.route('/sum', methods=['GET'])
def get_sums():
    sums = Sum.query.all()
    return jsonify([{"id": s.id, "a": s.a, "b": s.b, "result": s.result} for s in sums])

@app.route('/sum/result/<int:result>', methods=['GET'])
def get_sums_by_result(result):
    sums = Sum.query.filter_by(result=result).all()
    return jsonify([{"id": s.id, "a": s.a, "b": s.b, "result": s.result} for s in sums])

if __name__ == '__main__':
    app.run(debug=True)
