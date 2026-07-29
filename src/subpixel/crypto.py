import os
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
from .errors import DecryptionError

SALT_LEN = 16
NONCE_LEN = 12
KEY_LEN = 32 # AES-256

ARGON2_TIME_COST = 3
ARGON2_MEMORY_COST = 64 * 1024  # 64 MiB, in KiB
ARGON2_PARALLELISM = 4

def derive_key(password: str, salt: bytes):
    kdf = Argon2id(
        salt=salt,
        length=KEY_LEN,
        iterations=ARGON2_TIME_COST,
        lanes=ARGON2_PARALLELISM,
        memory_cost=ARGON2_MEMORY_COST,
    )
    return kdf.derive(password.encode("utf-8"))

def encrypt(plaintext: bytes, password: str) -> bytes:
    salt = os.urandom(SALT_LEN)
    nonce = os.urandom(NONCE_LEN)
    key = derive_key(password, salt)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, associated_data=None)
    return salt + nonce + ciphertext

def decrypt(blob: bytes, password: str) -> bytes:
    if len(blob) < SALT_LEN + NONCE_LEN:
        raise DecryptionError("Payload too short to contain salt/nonce")

    salt = blob[:SALT_LEN]
    nonce = blob[SALT_LEN:SALT_LEN + NONCE_LEN]
    ciphertext = blob[SALT_LEN + NONCE_LEN:]

    key = derive_key(password, salt)
    try:
        return AESGCM(key).decrypt(nonce, ciphertext, associated_data=None)
    except InvalidTag:
        raise DecryptionError("Wrong password or corrupted data")