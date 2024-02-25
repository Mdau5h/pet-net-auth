import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization as crypto_serialization
from dotenv import load_dotenv

load_dotenv()
KEYS = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)


class Config:

    PRIVATE_KEY: str = KEYS.private_bytes(
        crypto_serialization.Encoding.PEM, crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption()
    ).decode('utf-8')

    PUBLIC_KEY: str = KEYS.public_key().public_bytes(
        crypto_serialization.Encoding.PEM, crypto_serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM')

    TOKEN_EXPIRE_TIME_MINUTES: int = int(os.getenv('TOKEN_EXPIRE_TIME_MINUTES'))
    HOST: str = os.getenv('HOST')
    PORT: int = int(os.getenv('PORT'))
    SALT_ROUND: int = int(os.getenv('SALT_ROUND'))
    DB_NAME: str = os.getenv('DB_NAME')
    DB_URL: str = f'sqlite+aiosqlite:///{DB_NAME}'


config = Config()
