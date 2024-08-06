# Fund Management System

## Introduction
This project is a backend service for managing investment funds. It is built using Flask and provides RESTful API endpoints for CRUD operations.

## Installation
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd <cloned-folder-name>

2. Set up a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate 

4. Install dependencies:
   ```sh
   pip install -r requirements.txt

## Running the Application
1. Initialize the database:
   ```sh
   python migrate_data.py

2. Start the Flask application:
   python app.py
   The API will be available at http://127.0.0.1:5000.

## API Endpoints
1. Retrieve All Funds:
   URL: /funds
   Method: GET

2. Create a New Fund:
   URL: /funds
   Method: POST

3. Retrieve Fund by ID:
   URL: /funds/<int:fund_id>
   Method: GET

4. Update Fund Performance by ID:
   URL: /funds/<int:fund_id>
   Method: PUT

5. Delete Fund by ID:
   URL: /funds/<int:fund_id>
   Method: DELETE

## Testing
Running Tests:
```sh
python testing.py
