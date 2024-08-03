import pyodbc
from flask import current_app, g

def get_db_connection():
    try:
        if 'db_connection' not in g:
            connection_string = (
                f"DRIVER={{{current_app.config['DRIVER']}}};"
                f"SERVER={current_app.config['SQL_SERVER']},{current_app.config['PORT']};"
                f"DATABASE={current_app.config['DATABASE']};"
                f"UID={current_app.config['USERNAME']};"
                f"PWD={current_app.config['PASSWORD']};"
                f"Encrypt=yes;"
                f"TrustServerCertificate=no;"
                f"Connection Timeout=30;"
            )
            g.db_connection = pyodbc.connect(connection_string)
        return g.db_connection
    except pyodbc.Error as e:
        print(f"Database connection error: {e}")
        raise

def close_db_connection(exception):
    db_connection = g.pop('db_connection', None)
    if db_connection is not None:
        db_connection.close()
