import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

class Config:
    BASE_URL = os.getenv('BASE_URL')
    LOGIN_URL = os.getenv('LOGIN_URL')
    CHATS_URL = os.getenv('CHATS_URL')