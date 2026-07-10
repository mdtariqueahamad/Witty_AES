# 🔐 SecureVault — Offline Password Manager

A secure, offline desktop password manager with a stunning **glassmorphism** GUI. Built with Python, PyWebView, and military-grade AES-256 encryption.

---

## ✨ Features

| Feature | Description |
|---|---|
| **AES-256 Encryption** | All passwords are encrypted using Fernet (AES-256-CBC + HMAC-SHA256) |
| **PBKDF2 Key Derivation** | Master password is transformed via PBKDF2HMAC with 480,000 iterations |
| **Zero Plaintext Storage** | Only ciphertext stored in the database — even SQLite viewers show gibberish |
| **Glassmorphism UI** | Premium frosted glass design with animated gradients, blur effects, and micro-animations |
| **Password Generator** | Cryptographically secure random passwords with adjustable length (8–64 chars) |
| **Change Master Password** | Securely change your master password with full re-encryption of all stored credentials |
| **Clipboard Auto-Clear** | Copied passwords are automatically cleared from clipboard after 15 seconds |
| **Search & Filter** | Instantly search credentials by website or username |
| **Brute-Force Protection** | Locks out after 5 failed login attempts |
| **Password Strength Meter** | Real-time feedback while creating the master password |
| **3-Panel Dashboard** | Sidebar navigation, credential list, and detail panel — like a premium app |

---

## 📁 Project Structure

```
Password Manager/
├── main.py                 # Application entry point + PyWebView BackendAPI
├── ui/
│   └── index.html          # Glassmorphism frontend (HTML/CSS/JS)
├── crypto_engine.py        # Encryption, decryption, key derivation
├── database.py             # SQLite3 database operations
├── password_generator.py   # Secure random password generation
├── requirements.txt        # Python dependencies
├── vault.db                # (Created at runtime) Encrypted credential store
└── README.md               # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ installed
- `pip` package manager

### Installation

```bash
# 1. Navigate to the project directory
cd "Password Manager"

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# macOS / Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python main.py
```

### First Run
1. A **"Create Your Vault"** screen will appear with a frosted glass card
2. Set a strong Master Password (minimum 8 characters)
3. Confirm the password and click **"Create Vault"**
4. You're in! Start adding credentials via the **"+ Add New"** button

### Subsequent Runs
1. The **"Unlock SecureVault"** screen appears
2. Enter your Master Password to decrypt and access your credentials

---

## 📦 Required Packages

```
pywebview>=5.0.0            # Native desktop window with HTML/CSS/JS frontend
cryptography>=41.0.0        # Fernet AES-256 encryption + PBKDF2
pyperclip>=1.8.2            # Cross-platform clipboard access
```

Install all at once:
```bash
pip install pywebview cryptography pyperclip
```

---

## 🏗️ Building a Standalone .exe (Windows)

### Install PyInstaller
```bash
pip install pyinstaller
```

### Build Command
```bash
pyinstaller --onefile --windowed --name SecureVault --add-data "ui;ui" main.py
```

> **Note (macOS/Linux):** Use a colon `:` instead of semicolon `;` as the path separator:
> ```bash
> pyinstaller --onefile --windowed --name SecureVault --add-data "ui:ui" main.py
> ```

**Flags explained:**
| Flag | Purpose |
|---|---|
| `--onefile` | Bundle everything into a single `.exe` file |
| `--windowed` | Suppress the console window (GUI-only) |
| `--name SecureVault` | Name the output executable |
| `--add-data "ui;ui"` | Include the `ui/` folder with the HTML frontend |

The compiled executable will be in the `dist/` folder:
```
dist/
└── SecureVault.exe
```

> **Note:** The `vault.db` file is created at runtime in the same directory as the executable. Distribute the `.exe` alone — the database is created on first launch.

---

## 🔒 Security Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    User enters Master Password              │
└──────────────────────────┬─────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │  PBKDF2HMAC │  480,000 iterations
                    │   SHA-256   │  + 16-byte random salt
                    └──────┬──────┘
                           │
              ┌────────────┼────────────────┐
              │                             │
    ┌─────────▼─────────┐       ┌───────────▼───────────┐
    │  Verification Hash │       │  256-bit Fernet Key    │
    │  (stored in DB)    │       │  (held in memory only) │
    └────────────────────┘       └───────────┬───────────┘
                                             │
                                    ┌────────▼────────┐
                                    │  Fernet Engine   │
                                    │  AES-256-CBC     │
                                    │  + HMAC-SHA256   │
                                    └────────┬────────┘
                                             │
                                    ┌────────▼────────┐
                                    │  Encrypted       │
                                    │  ciphertext      │
                                    │  stored in DB    │
                                    └─────────────────┘
```

### What's stored in `vault.db`:
- ✅ Random salt (16 bytes)
- ✅ Verification hash (SHA-256 of salt + master password)
- ✅ Website names (plaintext — for search/display)
- ✅ Usernames (plaintext — for search/display)
- ✅ Encrypted passwords (Fernet ciphertext — unreadable without the key)

### What's NEVER stored:
- ❌ Master password (plaintext)
- ❌ Encryption key
- ❌ Plaintext passwords

---

## 🔑 Change Master Password

The Change Master Password feature (Settings → Change Master Password) performs a **full re-encryption**:

1. Verifies the current master password
2. Derives the old decryption key
3. Generates a NEW salt and derives a new encryption key
4. Decrypts ALL stored passwords using the old key
5. Re-encrypts ALL passwords using the new key
6. Updates the database with new ciphertext, salt, and verification hash

This ensures all credentials remain secure under the new master password.

---

## 🛡️ Security Best Practices

1. **Choose a strong Master Password** — at least 12+ characters with mixed case, digits, and symbols
2. **Don't share your Master Password** — there is no recovery mechanism
3. **Back up `vault.db`** — losing this file means losing all stored credentials
4. **The encryption key exists only in memory** — closing the app erases it
5. **Passwords auto-clear from clipboard** — copied passwords are cleared after 15 seconds

---

## 📄 License

This project is provided as-is for personal and educational use.
