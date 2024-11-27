import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Banco de Dados
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:oRMWkedPkaDBCDUTuYvMsPQFvpqtJWaf@postgres.railway.internal:5432/railway"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Debug
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1"]

    # Chave Secreta
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "a7e34f6c9b2d8e01f12d9c78b56d4a2c5f9a7b30c6e2d8f4b34e29d6a7f01c3e"
    )
