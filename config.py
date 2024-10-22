import os

class Config:
    # MySQL connection parameters
    SQL_SERVER = 'localhost'
    DATABASE = 'FamilyExpenses'
    USERNAME = 'ihoradmin'
    PASSWORD = 'DBExpenseslogin#'
    PORT = 3306  # Стандартний порт для MySQL

    # SQLAlchemy connection string for MySQL
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{USERNAME}:{PASSWORD}@{SQL_SERVER}:{PORT}/{DATABASE}"
    )

    # Logging configuration
    LOGGING_LEVEL = 'DEBUG'
    LOG_FILE = 'app.log'

    # Secret key for session management
    SECRET_KEY = os.urandom(24)  # Generates a random secret key
