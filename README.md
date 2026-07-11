# 🔐 SecureVault — Offline Password Manager

Welcome to **SecureVault**, an ultra-secure, completely offline desktop password manager that combines military-grade encryption with a stunning, premium user interface. 

Built with **Python**, **PyWebView**, and **SQLite**, it never connects to the internet. Your passwords stay on your device, locked behind a single Master Password.

---

## 🌟 Why SecureVault?

Most password managers live in the cloud. While convenient, this makes them targets for massive data breaches. SecureVault takes a different approach: **100% offline storage**. 

Coupled with a **Dynamic Cyber Environment**—featuring an animated Matrix-style background and premium frosted glass ("glassmorphism") UI elements—it feels like a high-end application while providing zero-knowledge security.

---

## ✨ Core Features

### 🛡️ Uncompromising Security
* **AES-256-CBC Encryption:** The gold standard in cryptographic security, ensuring your data is mathematically uncrackable.
* **Zero Plaintext Storage:** The database (`vault.db`) only stores scrambled ciphertext. Even if someone steals your computer, they cannot read your passwords.
* **Clipboard Auto-Clear:** Copied passwords automatically vanish from your clipboard after 15 seconds to prevent accidental pasting or snooping.
* **Brute-Force Protection:** The application locks out after 5 failed login attempts.

### 💎 Premium User Experience
* **Watery Glassmorphism UI:** A sleek, frosted glass interface (`blur(24px) saturate(120%)`) that beautifully refracts the background elements.
* **Dynamic Cyber Environment:** A highly engineered, animated cryptographic background featuring drifting data streams and a decentralized cybersecurity SVG mesh.
* **In-Place Dynamic Filtering:** Instantly view passwords by Category (e.g., Work, Social) or Security Tier (e.g., Weak, Reused) without clunky page reloads.
* **Unified Detail View:** Click any password to open a smooth, expanding card overlay for a read-only detailed view.

### 🛠️ Powerful Tools
* **Built-in Password Generator:** Generate cryptographically secure passwords (8–64 characters) with a single click.
* **Change Master Password:** Securely change your master password. The app will seamlessly re-encrypt all your stored credentials with a brand new key.
* **Password Strength Analyzer:** Automatically categorizes your saved passwords into Strong, Good, Weak, or Reused.

---

## 🚀 How to Get Started

### Prerequisites
Make sure you have **Python 3.10** (or newer) installed on your system.

### 1. Installation
Open your terminal or command prompt and run the following commands:

```bash
# 1. Navigate into the project folder
cd "Password Manager"

# 2. Create a virtual environment (keeps dependencies isolated)
python -m venv venv

# 3. Activate the virtual environment
# On macOS / Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install the required packages
pip install -r requirements.txt
```

### 2. Running the App
Once installed, simply run:
```bash
python main.py
```

### 3. Your First Run
1. When the app opens, you will see a **"Create Your Vault"** screen.
2. Enter a highly secure **Master Password**. This is the *only* password you will ever need to remember. 
3. *Note: Because this app is completely offline, there is NO "Forgot Password" button. Do not forget your Master Password!*
4. Click **Create Vault** and start adding your credentials!

---

## 🏗️ How to Build a Standalone Executable (.exe / .app)

If you don't want to run the app via the command line every time, you can bundle it into a standalone clickable application using PyInstaller.

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Build the Application:**
   * **For Windows:**
     ```bash
     pyinstaller --onefile --windowed --name SecureVault --add-data "ui;ui" main.py
     ```
   * **For macOS / Linux (Note the colon `:` instead of semicolon):**
     ```bash
     pyinstaller --onefile --windowed --name SecureVault --add-data "ui:ui" main.py
     ```

3. **Locate your App:**
   Inside the newly created `dist/` folder, you will find your standalone `SecureVault` executable. You can move this file anywhere on your computer. The `vault.db` database will automatically be created next to wherever the executable is run.

---

## 🔒 Under the Hood: Security Architecture

Here is exactly what happens when you use SecureVault:

1. **Key Derivation:** When you enter your Master Password, it is mathematically stretched 480,000 times using an algorithm called **PBKDF2HMAC** alongside a 16-byte random salt. This creates your 256-bit encryption key.
2. **Memory Only:** This key is *only* held in your computer's temporary memory (RAM). It is never saved to a file. When you close the app, the key disappears.
3. **Encryption:** When you save a new password, the app uses **Fernet (AES-256-CBC + HMAC-SHA256)** to scramble it using your key.
4. **Storage:** Only the scrambled, unreadable ciphertext is saved to the SQLite database (`vault.db`).

### What is stored in `vault.db`?
* ✅ The random salt (needed to rebuild the key).
* ✅ A verification hash (so the app knows if you typed the correct Master Password).
* ✅ Plaintext Website names and Usernames (so you can search them).
* ✅ **Scrambled Ciphertext** (your actual passwords, completely unreadable).

### What is NEVER stored?
* ❌ Your Master Password.
* ❌ Your Encryption Key.
* ❌ Your actual saved passwords.

---

## 🛡️ Best Practices for Keeping Your Data Safe

* **Choose a strong Master Password:** Use a mix of uppercase, lowercase, numbers, and symbols. Ideally, use a long "passphrase" (e.g., `Correct-Horse-Battery-Staple!`).
* **Backup your vault:** Simply copy the `vault.db` file to a USB drive or a safe location. If your computer breaks and you don't have a backup of `vault.db`, your passwords are gone forever.
* **Keep your computer secure:** Because the encryption key lives in your computer's memory while the app is open, make sure your computer itself is free of malware or spyware.

---

*Secured by WittyArtist.*
