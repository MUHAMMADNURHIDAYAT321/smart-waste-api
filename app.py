
from flask import Flask, jsonify
from sqlalchemy import event
from config import Config
from models import db
from routes import api


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    app.register_blueprint(api, url_prefix="/api")

    with app.app_context():

        if db.engine.dialect.name == "sqlite":

            @event.listens_for(db.engine, "connect")
            def enable_foreign_keys(connection, record):
                cursor = connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

        db.create_all()

    @app.route("/")
    def index():
        return jsonify({
            "success": True,
            "message": "Smart Waste Monitoring API",
            "version": "1.0"
        })

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "success": False,
            "message": "Endpoint tidak ditemukan"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({
            "success": False,
            "message": "HTTP method tidak diizinkan"
        }), 405

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)