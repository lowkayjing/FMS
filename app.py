from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///funds.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class InvestmentFund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    manager_name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    nav = db.Column(db.Float, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    performance = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "fund_id": self.id,
            "name": self.name,
            "manager_name": self.manager_name,
            "description": self.description,
            "nav": self.nav,
            "creation_date": self.creation_date.isoformat(),
            "performance": self.performance
        }

with app.app_context():
    db.create_all()

@app.route('/funds', methods=['GET'])
def get_funds():
    funds = InvestmentFund.query.all()
    return jsonify([fund.to_dict() for fund in funds])

@app.route('/funds', methods=['POST'])
def create_fund():
    data = request.json

    required_fields = ['name', 'manager_name', 'description', 'nav', 'performance']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        new_fund = InvestmentFund(
            name=data['name'],
            manager_name=data['manager_name'],
            description=data['description'],
            nav=float(data['nav']),
            performance=float(data['performance'])
        )
        db.session.add(new_fund)
        db.session.commit()
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid data types provided'}), 400

    return jsonify(new_fund.to_dict()), 201

@app.route('/funds/<int:fund_id>', methods=['GET'])
def get_fund(fund_id):
    fund = db.session.get(InvestmentFund, fund_id)
    if fund is None:
        return jsonify({'error': 'Fund not found'}), 404
    return jsonify(fund.to_dict())

@app.route('/funds/<int:fund_id>', methods=['PUT'])
def update_fund_performance(fund_id):
    fund = db.session.get(InvestmentFund, fund_id)
    if fund is None:
        return jsonify({'error': 'Fund not found'}), 404
    data = request.json
    try:
        fund.performance = float(data['performance'])
        db.session.commit()
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid data type for performance'}), 400
    return jsonify(fund.to_dict())

@app.route('/funds/<int:fund_id>', methods=['DELETE'])
def delete_fund(fund_id):
    fund = db.session.get(InvestmentFund, fund_id)
    if fund is None:
        return jsonify({'error': 'Fund not found'}), 404
    db.session.delete(fund)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
