import pyodbc
from flask import current_app, g

def get_db_connection():
    if 'db_connection' not in g:
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={current_app.config['SQL_SERVER']};"
            f"DATABASE={current_app.config['DATABASE']};"
            f"Trusted_Connection={current_app.config['TRUSTED_CONNECTION']};"
        )
        g.db_connection = pyodbc.connect(connection_string)
    return g.db_connection

def close_db_connection(exception):
    db_connection = g.pop('db_connection', None)
    if db_connection is not None:
        db_connection.close()
