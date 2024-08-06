from app import db, InvestmentFund, app

# Sample in-memory data
in_memory_data = [
    {
        "name": "Fund A",
        "manager_name": "Manager A",
        "description": "Description A",
        "nav": 100.0,
        "performance": 5.0
    },
    {
        "name": "Fund B",
        "manager_name": "Manager B",
        "description": "Description B",
        "nav": 200.0,
        "performance": 10.0
    }
]

def migrate_data():
    with app.app_context():
        if InvestmentFund.query.count() == 0:
            for fund_data in in_memory_data:
                new_fund = InvestmentFund(
                    name=fund_data['name'],
                    manager_name=fund_data['manager_name'],
                    description=fund_data['description'],
                    nav=fund_data['nav'],
                    performance=fund_data['performance']
                )
                db.session.add(new_fund)
            db.session.commit()
            print("Data migration complete.")
        else:
            print("Data already migrated.")

if __name__ == "__main__":
    migrate_data()
