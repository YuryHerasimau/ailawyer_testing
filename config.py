import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    # Загружаем .env файл
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    # Значения по умолчанию для CI
    BASE_URL = os.getenv('BASE_URL', 'https://app.ailawyer.pro')
    LOGIN_URL = os.getenv('LOGIN_URL', f'{BASE_URL}/login/')
    CHATS_URL = os.getenv('CHATS_URL', f'{BASE_URL}/chats/')