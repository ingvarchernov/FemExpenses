import os

class Config:
    # Параметри підключення до бази даних SQL Server
    SQL_SERVER = 'localhost\MSSQLSERVER01'
    DATABASE = 'FamilyExpenses'
    DRIVER = 'ODBC Driver 17 for SQL Server'
    TRUSTED_CONNECTION = 'yes'

    # Строка підключення
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{SQL_SERVER}/{DATABASE}"
        f"?driver={DRIVER}"
        f"&trusted_connection={TRUSTED_CONNECTION}"
    )

    # Налаштування логування
    LOGGING_LEVEL = 'DEBUG'
    LOG_FILE = 'app.log'

    # Секретний ключ для сесій
    SECRET_KEY = os.urandom(24)  # Генерує випадковий секретний ключ
