from flask import Flask
from database import db, init_db
from routes.users import users_bp
from routes.registros import registros_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fin_api.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'super-secret-key-change-me'  # change in production
    db.init_app(app)
    init_db(app)
    app.register_blueprint(users_bp, url_prefix='/')
    app.register_blueprint(registros_bp, url_prefix='/')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)