FastAPI Orders Service
=====================

This is a FastAPI-based order management service with MySQL database integration. 
It supports creating orders, fetching orders, and integrating with external APIs 
for product details.

Project Structure
-----------------
app/
  ├── api/               # FastAPI routers
  ├── core/              # Configuration and database setup
  ├── models/            # SQLAlchemy models
  ├── repository/        # CRUD operations
  ├── schemas/           # Pydantic schemas
  └── services/          # Business logic / service layer

tests/
  ├── test_orders_integration.py  # Integration test for order service

.env                   # Environment variables for development
.env.test              # Environment variables for testing

Requirements
------------
- Python 3.12+
- MySQL server
- pip packages in requirements.txt (FastAPI, SQLAlchemy, PyMySQL, pytest, etc.)

Setup
-----
1. Clone the repository:

   git clone <your-repo-url>
   cd fastapi-orders

2. Create virtual environment and activate:

   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows

3. Install dependencies:

   pip install -r requirements.txt

4. Configure environment variables:

   Copy `.env.example` to `.env` and `.env.test` for development and testing.
   Update MySQL credentials if needed.

   Example `.env`:

     APP_ENV=development
     MYSQL_USER=root
     MYSQL_PASSWORD=your_password
     MYSQL_HOST=localhost
     MYSQL_DB=orders_db
     APP_PORT=8000

   Example `.env.test`:

     APP_ENV=test
     MYSQL_USER=root
     MYSQL_PASSWORD=your_password
     MYSQL_HOST=localhost
     MYSQL_DB=orders_db_test
     APP_PORT=8001

Database Setup
--------------
1. Make sure MySQL is running.
2. Create the development and test databases:

   mysql -u root -p
   CREATE DATABASE orders_db;
   CREATE DATABASE orders_db_test;

3. The application automatically creates tables when started.

Running the App
---------------
1. Start the FastAPI app:

   uvicorn app.main:app --reload

2. Open API docs at:

   http://127.0.0.1:8000/docs

Running Tests
-------------
1. Ensure the test database exists (`orders_db_test`).
2. Run tests using pytest:

   export APP_ENV=test   # Linux/Mac
   set APP_ENV=test      # Windows

   pytest -v tests/test_orders_integration.py

Notes
-----
- The service uses SQLAlchemy for ORM and PyMySQL for MySQL connection.
- Environment variables control the database and port settings.
- External API calls are mocked in tests to ensure fast and reliable tests.


