import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import upgrade

from config import Config
from extensions import db, migrate
from routes import bp as routes_blueprint

logging.basicConfig(level=logging.DEBUG)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Permitir CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar rotas
    app.register_blueprint(routes_blueprint)

    with app.app_context():
        try:
            upgrade()  # Executa as migrations automaticamente
        except Exception as e:
            app.logger.error(f"Erro ao aplicar as migrations: {e}")

    @app.route('/test-db')
    def test_db():
        try:
            conn = db.engine.connect()
            conn.close()
            return "Conexão com o banco de dados bem-sucedida!", 200
        except Exception as e:
            return f"Erro ao conectar ao banco de dados: {str(e)}", 500

    @app.route('/health')
    def health_check():
        app.logger.debug("Health check endpoint chamado.")
        return {"status": "healthy"}, 200

    return app


# Instância global do app para produção
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
