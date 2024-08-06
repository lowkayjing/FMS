import unittest
from app import app, db, InvestmentFund
from migrate_data import migrate_data

class InvestmentFundTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_funds.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        print("Teardown complete")

    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            # Ensure the data is migrated before each test
            if InvestmentFund.query.count() == 0:
                migrate_data()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_fund(self):
        response = self.app.post('/funds', json={
            'name': 'Test Fund',
            'manager_name': 'John Doe',
            'description': 'A test fund',
            'nav': 100.0,
            'performance': 5.0
        })
        print(f"Create fund response: {response.status_code}")
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['name'], 'Test Fund')

    def test_get_fund(self):
        with app.app_context():
            fund = InvestmentFund(name='Test Fund', manager_name='John Doe', description='A test fund', nav=100.0, performance=5.0)
            db.session.add(fund)
            db.session.commit()
            fund_id = fund.id

        response = self.app.get(f'/funds/{fund_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], 'Test Fund')
        self.assertIsNotNone(data['creation_date'])

    def test_update_fund_performance(self):
        with app.app_context():
            fund = InvestmentFund(name='Test Fund', manager_name='John Doe', description='A test fund', nav=100.0, performance=5.0)
            db.session.add(fund)
            db.session.commit()
            fund_id = fund.id

        response = self.app.put(f'/funds/{fund_id}', json={'performance': 10.0})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['performance'], 10.0)

    def test_delete_fund(self):
        with app.app_context():
            fund = InvestmentFund(name='Test Fund', manager_name='John Doe', description='A test fund', nav=100.0, performance=5.0)
            db.session.add(fund)
            db.session.commit()
            fund_id = fund.id

        response = self.app.delete(f'/funds/{fund_id}')
        self.assertEqual(response.status_code, 204)

    def test_migrate_data(self):
        with app.app_context():
            funds = InvestmentFund.query.all()
            self.assertEqual(len(funds), 2)
            self.assertEqual(funds[0].name, 'Fund A')
            self.assertEqual(funds[1].name, 'Fund B')

    def test_invalid_get_fund(self):
        response = self.app.get('/funds/999')
        self.assertEqual(response.status_code, 404)

    def test_invalid_update_fund(self):
        response = self.app.put('/funds/999', json={'performance': 10.0})
        self.assertEqual(response.status_code, 404)

    def test_invalid_delete_fund(self):
        response = self.app.delete('/funds/999')
        self.assertEqual(response.status_code, 404)

    def test_empty_create_fund(self):
        response = self.app.post('/funds', json={})
        self.assertEqual(response.status_code, 400)

    def test_partial_create_fund(self):
        response = self.app.post('/funds', json={
            'name': 'Partial Fund'
        })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main(verbosity=2)
