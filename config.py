import os

class Config:
    # SQL Server connection parameters
    SQL_SERVER = 'sqlserverexpenses.database.windows.net'
    DATABASE = 'FamilyExpenses'
    USERNAME = 'ihoradmin'
    PASSWORD = 'DBExpenseslogin#'
    DRIVER = 'ODBC Driver 18 for SQL Server'  # Ensure this matches the driver you installed
    PORT = 1433

    # SQLAlchemy connection string
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SQL_SERVER}:{PORT}/{DATABASE}"
        f"?driver={DRIVER}"
        f"&Encrypt=yes"
        f"&TrustServerCertificate=no"
        f"&Connection Timeout=30"
    )

    # Logging configuration
    LOGGING_LEVEL = 'DEBUG'
    LOG_FILE = 'app.log'

    # Secret key for session management
    SECRET_KEY = os.urandom(24)  # Generates a random secret key
