"""
main.py — Entry point for the SecureVault Password Manager.

This script bootstraps the application by creating a PyWebView window
with a Python backend API that bridges the HTML/CSS/JS frontend to the
crypto engine and SQLite database.

The BackendAPI class exposes methods that the JavaScript frontend calls
via `window.pywebview.api.method_name()`.

Usage:
    python main.py

PyInstaller:
    pyinstaller --onefile --windowed --name SecureVault \
        --add-data "ui:ui" \
        main.py
"""

import sys
import os
import threading
from typing import Optional

# pyrefly: ignore [missing-import]
import webview
import pyperclip

from crypto_engine import (
    generate_salt,
    derive_key,
    create_verification_hash,
    verify_master_password,
    encrypt_password,
    decrypt_password,
)
from database import (
    initialize_database,
    vault_exists,
    save_master_config,
    get_master_config,
    add_credential,
    get_all_credentials,
    get_all_credential_ids_and_passwords,
    get_favorites,
    search_credentials,
    update_credential,
    update_credential_password,
    update_credential_category,
    update_master_config,
    delete_credential,
    toggle_favorite,
)
from password_generator import generate_password
from categorizer import auto_categorize
from strength_analyzer import analyze_strength, analyze_all

def resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a resource, works for both development
    and PyInstaller bundled executables.

    PyInstaller creates a temp folder and stores the path in sys._MEIPASS.
    """
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except AttributeError:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

class BackendAPI:
    """
    Python backend API that the JavaScript frontend communicates with.

    Each method returns a dict that gets serialized to JSON automatically
    by PyWebView. The JS frontend calls these via:
        window.pywebview.api.method_name(args)
    """

    def __init__(self) -> None:
        self.encryption_key: Optional[bytes] = None
        self._clipboard_timer: Optional[threading.Timer] = None

    def check_vault(self) -> dict:
        """Check if a vault already exists (has master config)."""
        return {"exists": vault_exists()}

    # Setup — First-run master password creation

    def setup_vault(self, master_password: str) -> dict:
        """
        Create a new vault with the given master password.

        Generates a salt, creates the verification hash, and stores
        them in the database. Derives the encryption key and holds
        it in memory.
        """
        try:
            salt = generate_salt()
            verification_hash = create_verification_hash(master_password, salt)
            save_master_config(salt, verification_hash)
            self.encryption_key = derive_key(master_password, salt)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # Login — Unlock the vault

    def login(self, master_password: str) -> dict:
        """
        Verify the master password and derive the encryption key.

        Returns success if the password matches the stored hash.
        """
        try:
            config = get_master_config()
            if config is None:
                return {"success": False, "error": "Vault configuration not found."}

            salt, stored_hash = config

            if verify_master_password(master_password, salt, stored_hash):
                self.encryption_key = derive_key(master_password, salt)
                return {"success": True}
            else:
                return {"success": False, "error": "Incorrect master password."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # Lock — Clear the encryption key

    def lock_vault(self) -> dict:
        """Clear the encryption key from memory (lock the vault)."""
        self.encryption_key = None
        return {"success": True}

    # Credentials — CRUD Operations

    def get_credentials(self) -> dict:
        """
        Get all credentials with decrypted password length, favorite status,
        and auto-categorized category.
        """
        try:
            rows = get_all_credentials()
            creds = []
            for row in rows:
                # Decrypt to get password length for strength display
                try:
                    if self.encryption_key:
                        decrypted = decrypt_password(row["password_enc"], self.encryption_key)
                        pw_len = len(decrypted)
                    else:
                        pw_len = 0
                except Exception:
                    pw_len = 0

                # Auto-categorize if category is empty
                category = row["category"] if row["category"] else auto_categorize(row["website"])

                creds.append({
                    "id": row["id"],
                    "website": row["website"],
                    "username": row["username"],
                    "password_length": pw_len,
                    "is_favorite": row["is_favorite"],
                    "category": category,
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                })
            return {"success": True, "credentials": creds}
        except Exception as e:
            return {"success": False, "credentials": [], "error": str(e)}

    def get_credential_detail(self, cred_id: int) -> dict:
        """Get full detail for a single credential (without decrypted password)."""
        try:
            rows = get_all_credentials()
            for row in rows:
                if row["id"] == cred_id:
                    category = row["category"] if row["category"] else auto_categorize(row["website"])
                    return {
                        "success": True,
                        "credential": {
                            "id": row["id"],
                            "website": row["website"],
                            "username": row["username"],
                            "is_favorite": row["is_favorite"],
                            "category": category,
                            "created_at": row["created_at"],
                            "updated_at": row["updated_at"],
                        }
                    }
            return {"success": False, "error": "Credential not found."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def add_credential(self, website: str, username: str, password: str,
                       category: str = "") -> dict:
        """Encrypt and store a new credential with auto-categorization."""
        try:
            if not self.encryption_key:
                return {"success": False, "error": "Vault is locked."}
            encrypted = encrypt_password(password, self.encryption_key)
            # Auto-categorize if no category provided
            if not category:
                category = auto_categorize(website)
            row_id = add_credential(website, username, encrypted, category=category)
            return {"success": True, "id": row_id}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def edit_credential(self, cred_id: int, website: str, username: str,
                        password: str, category: str = "") -> dict:
        """Update an existing credential with new encrypted data."""
        try:
            if not self.encryption_key:
                return {"success": False, "error": "Vault is locked."}
            encrypted = encrypt_password(password, self.encryption_key)
            if not category:
                category = auto_categorize(website)
            update_credential(cred_id, website, username, encrypted, category=category)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete_credential(self, cred_id: int) -> dict:
        """Delete a credential by ID."""
        try:
            delete_credential(cred_id)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # Favorites

    def toggle_favorite(self, cred_id: int, is_favorite: int) -> dict:
        """Toggle the favorite status of a credential."""
        try:
            toggle_favorite(cred_id, is_favorite)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_favorites(self) -> dict:
        """Get only favorited credentials."""
        try:
            rows = get_favorites()
            creds = []
            for row in rows:
                try:
                    if self.encryption_key:
                        decrypted = decrypt_password(row["password_enc"], self.encryption_key)
                        pw_len = len(decrypted)
                    else:
                        pw_len = 0
                except Exception:
                    pw_len = 0

                category = row["category"] if row["category"] else auto_categorize(row["website"])

                creds.append({
                    "id": row["id"],
                    "website": row["website"],
                    "username": row["username"],
                    "password_length": pw_len,
                    "is_favorite": row["is_favorite"],
                    "category": category,
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                })
            return {"success": True, "credentials": creds}
        except Exception as e:
            return {"success": False, "credentials": [], "error": str(e)}

    # Category Management

    def update_category(self, cred_id: int, category: str) -> dict:
        """Update a credential's category."""
        try:
            update_credential_category(cred_id, category)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_categories_summary(self) -> dict:
        """Get a summary of credentials grouped by category."""
        try:
            rows = get_all_credentials()
            category_counts: dict[str, int] = {}
            for row in rows:
                cat = row["category"] if row["category"] else auto_categorize(row["website"])
                category_counts[cat] = category_counts.get(cat, 0) + 1
            return {"success": True, "categories": category_counts}
        except Exception as e:
            return {"success": False, "categories": {}, "error": str(e)}

    # Security Report

    def get_security_report(self) -> dict:
        """
        Decrypt all passwords and analyze their strength.

        Returns credentials grouped by strength: strong, good, weak.
        """
        try:
            if not self.encryption_key:
                return {"success": False, "error": "Vault is locked."}

            rows = get_all_credentials()
            creds_with_passwords = []
            for row in rows:
                try:
                    decrypted = decrypt_password(row["password_enc"], self.encryption_key)
                except Exception:
                    decrypted = ""

                category = row["category"] if row["category"] else auto_categorize(row["website"])

                creds_with_passwords.append({
                    "id": row["id"],
                    "website": row["website"],
                    "username": row["username"],
                    "password": decrypted,
                    "category": category,
                })

            report = analyze_all(creds_with_passwords)
            return {
                "success": True,
                "strong": report["strong"],
                "good": report["good"],
                "weak": report["weak"],
                "total": len(creds_with_passwords),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # Password Display & Copy

    def show_password(self, cred_id: int) -> dict:
        """Decrypt and return a credential's password."""
        try:
            if not self.encryption_key:
                return {"success": False, "error": "Vault is locked."}
            rows = get_all_credentials()
            for row in rows:
                if row["id"] == cred_id:
                    decrypted = decrypt_password(row["password_enc"], self.encryption_key)
                    return {"success": True, "password": decrypted}
            return {"success": False, "error": "Credential not found."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def copy_password(self, cred_id: int) -> dict:
        """Decrypt a password and copy it to the system clipboard."""
        try:
            if not self.encryption_key:
                return {"success": False, "error": "Vault is locked."}
            rows = get_all_credentials()
            for row in rows:
                if row["id"] == cred_id:
                    decrypted = decrypt_password(row["password_enc"], self.encryption_key)
                    self._copy_with_auto_clear(decrypted)
                    return {"success": True}
            return {"success": False, "error": "Credential not found."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def copy_to_clipboard(self, text: str) -> dict:
        """Copy arbitrary text (e.g. username) to clipboard."""
        try:
            self._copy_with_auto_clear(text)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _copy_with_auto_clear(self, text: str) -> None:
        """Copy text to clipboard and auto-clear after 15 seconds."""
        try:
            pyperclip.copy(text)
        except pyperclip.PyperclipException:
            pass  # Clipboard not available

        # Cancel existing timer
        if self._clipboard_timer and self._clipboard_timer.is_alive():
            self._clipboard_timer.cancel()

        # Auto-clear after 15 seconds
        self._clipboard_timer = threading.Timer(15.0, self._clear_clipboard)
        self._clipboard_timer.daemon = True
        self._clipboard_timer.start()

    @staticmethod
    def _clear_clipboard() -> None:
        """Clear the system clipboard."""
        try:
            pyperclip.copy("")
        except Exception:
            pass

    # Password Generator

    def generate_password(self, length: int = 20) -> dict:
        """Generate a cryptographically secure random password."""
        try:
            password = generate_password(length=length)
            return {"success": True, "password": password}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # Change Master Password — CRITICAL SECURITY OPERATION

    def change_master_password(self, current_password: str, new_password: str) -> dict:
        """
        Change the master password with full re-encryption.

        This method:
        1. Verifies the current master password.
        2. Derives the old decryption key.
        3. Generates a new salt and derives a new encryption key.
        4. Decrypts ALL stored passwords with the old key.
        5. Re-encrypts ALL passwords with the new key.
        6. Updates the database with new ciphertext, salt, and hash.
        """
        try:
            if not self.encryption_key:
                return {"success": False, "error": "Vault is locked."}

            # Step 1: Verify current password
            config = get_master_config()
            if config is None:
                return {"success": False, "error": "Vault configuration not found."}

            old_salt, stored_hash = config

            if not verify_master_password(current_password, old_salt, stored_hash):
                return {"success": False, "error": "Current password is incorrect."}

            #Derive old key (for decryption)
            old_key = derive_key(current_password, old_salt)

            #new salt and derive new key
            new_salt = generate_salt()
            new_key = derive_key(new_password, new_salt)
            new_hash = create_verification_hash(new_password, new_salt)

            #Re-encrypt
            all_creds = get_all_credential_ids_and_passwords()
            for cred_id, password_enc in all_creds:
                # Decrypt with old key
                plaintext = decrypt_password(password_enc, old_key)
                # Re-encrypt with new key
                new_enc = encrypt_password(plaintext, new_key)
                # Update in database
                update_credential_password(cred_id, new_enc)

            # Step 6: Update master config
            update_master_config(new_salt, new_hash)

            # Update the in-memory key
            self.encryption_key = new_key

            return {"success": True}
        except Exception as e:
            return {"success": False, "error": f"Re-encryption failed: {str(e)}"}


    # Close App

    def close_app(self) -> None:
        """Close the application window (called after lockout)."""
        self.encryption_key = None
        os._exit(0)



# Application Entry Point

def main() -> None:
    """Initialize the database and launch the PyWebView window."""
    # Initialize the SQLite database (creates tables if needed)
    initialize_database()

    # Create the backend API instance
    api = BackendAPI()

    # Resolve the HTML file path (PyInstaller-compatible)
    html_path = resource_path(os.path.join("ui", "index.html"))

    # Create the PyWebView window
    window = webview.create_window(
        title="Witty AES — Password Manager",
        url=html_path,
        js_api=api,
        width=1100,
        height=720,
        min_size=(900, 600),
        background_color="#F4F3EF",
        text_select=False,
    )

    # Start the PyWebView event loop
    webview.start(debug=False)


if __name__ == "__main__":
    main()
