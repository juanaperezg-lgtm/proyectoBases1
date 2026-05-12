import hashlib
import hmac
import os


def hash_password(password: str, iterations: int = 120_000) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"{iterations}${salt.hex()}${digest.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    iterations_raw, salt_hex, digest_hex = password_hash.split("$")
    iterations = int(iterations_raw)
    salt = bytes.fromhex(salt_hex)
    expected = bytes.fromhex(digest_hex)
    current = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(current, expected)
