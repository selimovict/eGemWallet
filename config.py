import os
from dotenv import load_dotenv


# Bira env fajl na osnovu APP_ENV varijable.
#   APP_ENV nije postavljen  ->  .env
#   APP_ENV=production        ->  .env.production
#   APP_ENV=debug             ->  .env.debug
#   APP_ENV=staging           ->  .env.staging
_env_name = os.getenv("APP_ENV")
_dotenv_file = f".env.{_env_name}" if _env_name else ".env"
load_dotenv(_dotenv_file)


class Config:
    APP_ENV = _env_name or "default"

    DB_SERVER = os.getenv("DB_SERVER", "192.168.88.87")
    DB_PORT = int(os.getenv("DB_PORT", "1433"))
    DB_NAME = os.getenv("DB_NAME", "eGemWalletDb")
    DB_USER = os.getenv("DB_USER", "sa")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "19Zeljo21")

    FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    FLASK_PORT = int(os.getenv("FLASK_PORT", "9090"))
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
