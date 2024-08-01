# app/__init__.py
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
from app.user_routes import user_bp
from app.expenses_routes import expenses_bp
from app.main_routes import main_bp
from app.db import close_db_connection

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Налаштування логування
    if not app.debug:
        handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=10000, backupCount=1)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)

     # Імплементація blueprints
    from .user_routes import user_bp
    from .expenses_routes import expenses_bp
    from .main_routes import main_bp


    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(expenses_bp)
    app.register_blueprint(main_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    app.teardown_appcontext(close_db_connection)

    # Налаштування логування
    if not app.debug:
        # Логування в файл
        file_handler = RotatingFileHandler(
            app.config['LOG_FILE'], maxBytes=10240, backupCount=1
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        file_handler.setLevel(app.config['LOGGING_LEVEL'])
        app.logger.addHandler(file_handler)
        app.logger.setLevel(app.config['LOGGING_LEVEL'])

    # Реєстрація функції закриття з’єднання
    app.teardown_appcontext(close_db_connection)

    return app
