import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SALT_ROUND: int = int(os.getenv('SALT_ROUND'))
    DB_NAME: str = os.getenv('DB_NAME')
    DB_URL: str = f'sqlite+aiosqlite:///{DB_NAME}'


config = Config()
