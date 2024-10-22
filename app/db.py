import pymysql
from flask import current_app, g

def get_db_connection():
    try:
        if 'db_connection' not in g:
            # Підключення до бази даних MySQL
            g.db_connection = pymysql.connect(
                host=current_app.config['SQL_SERVER'],
                port=current_app.config['PORT'],
                user=current_app.config['USERNAME'],
                password=current_app.config['PASSWORD'],
                database=current_app.config['DATABASE'],
                cursorclass=pymysql.cursors.DictCursor
            )
        return g.db_connection
    except pymysql.MySQLError as e:
        print(f"Database connection error: {e}")
        raise

def close_db_connection(exception):
    db_connection = g.pop('db_connection', None)
    if db_connection is not None:
        db_connection.close()
