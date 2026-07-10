"""
crypto_engine.py — Handles all cryptographic operations for the Password Manager.

This module provides:
  - Master password hashing and verification via PBKDF2HMAC (SHA-256).
  - Fernet-based symmetric encryption/decryption (AES-256 in CBC mode).
  - Secure salt generation using os.urandom.

Security Design:
  - The master password is NEVER stored in plaintext.
  - A random 16-byte salt is generated once during vault setup.
  - PBKDF2HMAC with 480,000 iterations derives a 256-bit key from the master password.
  - A separate verification hash (using a different salt derivation) confirms the master
    password at login without exposing the encryption key.
"""

import os
import base64
import hashlib
import hmac
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SALT_SIZE = 16            # 128-bit salt
KDF_ITERATIONS = 480_000  # OWASP-recommended minimum for PBKDF2-SHA256


# ---------------------------------------------------------------------------
# Salt Generation
# ---------------------------------------------------------------------------
def generate_salt() -> bytes:
    """Generate a cryptographically secure random salt (16 bytes)."""
    return os.urandom(SALT_SIZE)


# ---------------------------------------------------------------------------
# Key Derivation
# ---------------------------------------------------------------------------
def derive_key(master_password: str, salt: bytes) -> bytes:
    """
    Derive a 256-bit Fernet-compatible key from the master password using PBKDF2HMAC.

    Args:
        master_password: The user's master password (plaintext).
        salt: A 16-byte random salt stored alongside the vault.

    Returns:
        A URL-safe base64-encoded 32-byte key suitable for Fernet.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode("utf-8")))
    return key


# ---------------------------------------------------------------------------
# Master Password Verification Hash
# ---------------------------------------------------------------------------
def create_verification_hash(master_password: str, salt: bytes) -> str:
    """
    Create a SHA-256 hash of the master password combined with the salt.

    This hash is stored in the database so we can verify the master password
    at login time WITHOUT storing the password itself or the encryption key.

    Args:
        master_password: The plaintext master password.
        salt: The vault's salt.

    Returns:
        A hex-encoded SHA-256 digest string.
    """
    combined = salt + master_password.encode("utf-8")
    return hashlib.sha256(combined).hexdigest()


def verify_master_password(master_password: str, salt: bytes, stored_hash: str) -> bool:
    """
    Verify a master password attempt against the stored verification hash.

    Args:
        master_password: The password attempt to verify.
        salt: The vault's salt (retrieved from DB).
        stored_hash: The hex-encoded hash stored during vault setup.

    Returns:
        True if the password matches; False otherwise.
    """
    candidate_hash = create_verification_hash(master_password, salt)
    # Constant-time comparison to prevent timing attacks
    return hmac.compare_digest(candidate_hash, stored_hash)


# ---------------------------------------------------------------------------
# Fernet Encryption / Decryption
# ---------------------------------------------------------------------------
def encrypt_password(plaintext: str, key: bytes) -> str:
    """
    Encrypt a plaintext password using Fernet (AES-256-CBC + HMAC).

    Args:
        plaintext: The password to encrypt.
        key: The Fernet key derived from the master password.

    Returns:
        A base64-encoded ciphertext string safe for database storage.
    """
    fernet = Fernet(key)
    token = fernet.encrypt(plaintext.encode("utf-8"))
    return token.decode("utf-8")


def decrypt_password(ciphertext: str, key: bytes) -> str:
    """
    Decrypt a Fernet-encrypted password back to plaintext.

    Args:
        ciphertext: The base64-encoded token from the database.
        key: The Fernet key derived from the master password.

    Returns:
        The original plaintext password.

    Raises:
        InvalidToken: If the key is wrong or the ciphertext has been tampered with.
    """
    fernet = Fernet(key)
    plaintext = fernet.decrypt(ciphertext.encode("utf-8"))
    return plaintext.decode("utf-8")
