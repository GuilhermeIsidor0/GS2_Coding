import os
from dotenv import load_dotenv

# Carrega as configurações do arquivo .env.
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER', ''),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'cidade_alerta'),
    'charset': 'utf8mb4',
    'connect_timeout': 8
}
