"""
database.py — SQLite3 database layer for the Password Manager vault.

This module manages two tables inside `vault.db`:

  1. `master_config` — Stores the salt and verification hash for the master password.
     Only ONE row ever exists in this table.

  2. `credentials` — Stores encrypted credentials with columns:
     - id          : Auto-increment primary key.
     - website     : The site/service name (plaintext for search/display).
     - username    : The login username (plaintext for search/display).
     - password_enc: The Fernet-encrypted password (ciphertext).
     - is_favorite : Whether this credential is starred (0 or 1).
     - category    : The category tag (e.g., "Social", "Finance", or "").
     - created_at  : Timestamp of when the entry was created.
     - updated_at  : Timestamp of the last update.

Security Note:
  - Only the `password_enc` column contains sensitive data, and it is always
    stored as Fernet ciphertext. Even if someone opens vault.db with an SQLite
    browser, they will see only unreadable base64-encoded ciphertext.
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional


# ---------------------------------------------------------------------------
# Database path — resolves relative to the script's directory so it works
# correctly when compiled into a PyInstaller bundle.
# ---------------------------------------------------------------------------
def _get_db_path() -> str:
    """Return the absolute path to vault.db alongside the executable/script."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "vault.db")


DB_PATH = _get_db_path()


# ---------------------------------------------------------------------------
# Connection helper
# ---------------------------------------------------------------------------
def _get_connection() -> sqlite3.Connection:
    """Create and return a connection to the vault database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    conn.execute("PRAGMA journal_mode=WAL;")  # Better concurrent access
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------
def initialize_database() -> None:
    """
    Create the database tables if they don't already exist.
    Also performs safe schema migrations for new columns.

    Called once at application startup.
    """
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS master_config (
            id              INTEGER PRIMARY KEY CHECK (id = 1),
            salt            BLOB    NOT NULL,
            verification_hash TEXT  NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            website         TEXT    NOT NULL,
            username        TEXT    NOT NULL,
            password_enc    TEXT    NOT NULL,
            created_at      TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
            updated_at      TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
    """)

    # --- Safe schema migration: add new columns if they don't exist ---
    # These ALTER TABLE statements are idempotent — they silently fail
    # if the column already exists.
    try:
        cursor.execute("ALTER TABLE credentials ADD COLUMN is_favorite INTEGER DEFAULT 0;")
    except sqlite3.OperationalError:
        pass  # Column already exists

    try:
        cursor.execute("ALTER TABLE credentials ADD COLUMN category TEXT DEFAULT '';")
    except sqlite3.OperationalError:
        pass  # Column already exists

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Master Config Operations
# ---------------------------------------------------------------------------
def vault_exists() -> bool:
    """Check whether vault.db exists AND has a master config row."""
    if not os.path.exists(DB_PATH):
        return False
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM master_config;")
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0


def save_master_config(salt: bytes, verification_hash: str) -> None:
    """
    Store the salt and verification hash during initial vault setup.

    Args:
        salt: The randomly generated salt (16 bytes).
        verification_hash: SHA-256 hex digest of (salt + master_password).
    """
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO master_config (id, salt, verification_hash) VALUES (1, ?, ?);",
        (salt, verification_hash),
    )
    conn.commit()
    conn.close()


def get_master_config() -> Optional[tuple]:
    """
    Retrieve the salt and verification hash from the database.

    Returns:
        A tuple (salt: bytes, verification_hash: str) or None if not set.
    """
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT salt, verification_hash FROM master_config WHERE id = 1;")
    row = cursor.fetchone()
    conn.close()
    if row:
        return (bytes(row["salt"]), row["verification_hash"])
    return None


def update_master_config(salt: bytes, verification_hash: str) -> None:
    """
    Update the master config with a new salt and verification hash.

    Used during the Change Master Password flow after all credentials
    have been re-encrypted with the new key.

    Args:
        salt: The new randomly generated salt (16 bytes).
        verification_hash: New SHA-256 hex digest of (salt + new_master_password).
    """
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE master_config SET salt = ?, verification_hash = ? WHERE id = 1;",
        (salt, verification_hash),
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Credential CRUD Operations
# ---------------------------------------------------------------------------
def add_credential(website: str, username: str, password_enc: str,
                   category: str = "", is_favorite: int = 0) -> int:
    """
    Insert a new encrypted credential into the vault.

    Args:
        website: The website/service name.
        username: The login username.
        password_enc: The Fernet-encrypted password string.
        category: The category tag (e.g., "Social", "Finance"). Defaults to "".
        is_favorite: Whether the credential is starred (0 or 1). Defaults to 0.

    Returns:
        The row ID of the newly inserted credential.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO credentials (website, username, password_enc, category, is_favorite, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?);""",
        (website, username, password_enc, category, is_favorite, now, now),
    )
    row_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return row_id


def get_all_credential_ids_and_passwords() -> list:
    """
    Retrieve only the id and encrypted password for all credentials.

    Used during the Change Master Password re-encryption flow to minimize
    the amount of data loaded into memory.

    Returns:
        A list of tuples: [(id, password_enc), ...].
    """
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_enc FROM credentials;")
    rows = [(row["id"], row["password_enc"]) for row in cursor.fetchall()]
    conn.close()
    return rows


def update_credential_password(cred_id: int, password_enc: str) -> None:
    """
    Update only the encrypted password for a specific credential.

    Used during the Change Master Password re-encryption flow.

    Args:
        cred_id: The primary key of the credential.
        password_enc: The new Fernet-encrypted password string.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE credentials SET password_enc = ?, updated_at = ? WHERE id = ?;",
        (password_enc, now, cred_id),
    )
    conn.commit()
    conn.close()


def get_all_credentials() -> list:
    """
    Retrieve all credentials from the vault.

    Returns:
        A list of sqlite3.Row objects with columns:
        id, website, username, password_enc, is_favorite, category, created_at, updated_at.
    """
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, website, username, password_enc, is_favorite, category, created_at, updated_at "
        "FROM credentials ORDER BY website COLLATE NOCASE ASC;"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_favorites() -> list:
    """
    Retrieve only favorited credentials from the vault.

    Returns:
        A list of sqlite3.Row objects where is_favorite == 1.
    """
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, website, username, password_enc, is_favorite, category, created_at, updated_at "
        "FROM credentials WHERE is_favorite = 1 ORDER BY website COLLATE NOCASE ASC;"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def toggle_favorite(cred_id: int, is_favorite: int) -> None:
    """
    Set or unset the favorite flag for a credential.

    Args:
        cred_id: The primary key of the credential.
        is_favorite: 1 to mark as favorite, 0 to unmark.
    """
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE credentials SET is_favorite = ? WHERE id = ?;",
        (is_favorite, cred_id),
    )
    conn.commit()
    conn.close()


def update_credential_category(cred_id: int, category: str) -> None:
    """
    Update the category for a specific credential.

    Args:
        cred_id: The primary key of the credential.
        category: The new category string.
    """
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE credentials SET category = ? WHERE id = ?;",
        (category, cred_id),
    )
    conn.commit()
    conn.close()


def search_credentials(query: str) -> list:
    """
    Search credentials by website or username (case-insensitive partial match).

    Args:
        query: The search string.

    Returns:
        A list of matching sqlite3.Row objects.
    """
    conn = _get_connection()
    cursor = conn.cursor()
    like_query = f"%{query}%"
    cursor.execute(
        """SELECT id, website, username, password_enc, is_favorite, category, created_at, updated_at
           FROM credentials
           WHERE website LIKE ? OR username LIKE ?
           ORDER BY website COLLATE NOCASE ASC;""",
        (like_query, like_query),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_credential(cred_id: int, website: str, username: str,
                      password_enc: str, category: str = "") -> None:
    """
    Update an existing credential in the vault.

    Args:
        cred_id: The primary key of the credential to update.
        website: The new website/service name.
        username: The new username.
        password_enc: The new Fernet-encrypted password string.
        category: The category tag. Defaults to "".
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE credentials
           SET website = ?, username = ?, password_enc = ?, category = ?, updated_at = ?
           WHERE id = ?;""",
        (website, username, password_enc, category, now, cred_id),
    )
    conn.commit()
    conn.close()


def delete_credential(cred_id: int) -> None:
    """
    Delete a credential from the vault by its ID.

    Args:
        cred_id: The primary key of the credential to remove.
    """
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM credentials WHERE id = ?;", (cred_id,))
    conn.commit()
    conn.close()
