from subpixel.crypto import encrypt, decrypt
from subpixel.errors import DecryptionError

import pytest

def test_crypto_round_trip():
    msg = "Hello World!"
    blob = encrypt(msg.encode("utf-8"), "password123123")
    assert decrypt(blob, "password123123").decode("utf-8") == msg

def test_multibyte_crypto():
    msg = "héllo 😛😛😛😛😛😛"
    blob = encrypt(msg.encode("utf-8"), "pass")
    assert decrypt(blob, "pass").decode("utf-8") == msg

def test_wrong_password_raises():
    blob = encrypt(b"secret", "correct-password")
    with pytest.raises(DecryptionError):
        decrypt(blob, "wrong-password")

def test_tampered_ciphertext_raises():
    blob = encrypt(b"secret", "password")
    tampered = bytearray(blob)
    tampered[-1] ^= 0xFF  # flip last byte of the tag
    with pytest.raises(DecryptionError):
        decrypt(bytes(tampered), "password")

def test_tampered_early_byte_raises():
    # flip a byte in the ciphertext body, not just the tag
    blob = encrypt(b"secret message here", "password")
    tampered = bytearray(blob)
    tampered[20] ^= 0xFF
    with pytest.raises(DecryptionError):
        decrypt(bytes(tampered), "password")

def test_encrypt_uses_fresh_salt_and_nonce():
    blob1 = encrypt(b"same message", "same-password")
    blob2 = encrypt(b"same message", "same-password")
    assert blob1 != blob2  # different salt/nonce -> different ciphertext
    assert blob1[:16] != blob2[:16]  # salts differ
    assert blob1[16:28] != blob2[16:28]  # nonces differ

def test_truncated_blob_raises_decryption_error():
    with pytest.raises(DecryptionError):
        decrypt(b"short", "password")

def test_empty_blob_raises_decryption_error():
    with pytest.raises(DecryptionError):
        decrypt(b"", "password")

def test_empty_message_round_trip():
    blob = encrypt(b"", "password")
    assert decrypt(blob, "password") == b""

def test_unicode_password_round_trip():
    msg = b"secret"
    password = "pásswörd日本語"
    blob = encrypt(msg, password)
    assert decrypt(blob, password) == msg

def test_password_is_case_sensitive():
    blob = encrypt(b"secret", "Password")
    with pytest.raises(DecryptionError):
        decrypt(blob, "password")