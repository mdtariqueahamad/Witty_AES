"""
password_generator.py — Secure random password generation.

Uses Python's `secrets` module (cryptographically secure) instead of `random`
to generate strong, unpredictable passwords.

Features:
  - Configurable length (default: 20 characters).
  - Guarantees at least one character from each category:
    uppercase, lowercase, digit, and special symbol.
  - Shuffles the result to avoid predictable patterns.
"""

import secrets
import string


# ---------------------------------------------------------------------------
# Character Sets
# ---------------------------------------------------------------------------
LOWERCASE = string.ascii_lowercase       # a-z
UPPERCASE = string.ascii_uppercase       # A-Z
DIGITS = string.digits                   # 0-9
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?"  # Common special characters


def generate_password(
    length: int = 20,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    """
    Generate a cryptographically secure random password.

    Args:
        length: Desired password length (minimum 8, default 20).
        use_uppercase: Include uppercase letters.
        use_digits: Include digits.
        use_symbols: Include special characters.

    Returns:
        A randomly generated password string.

    Raises:
        ValueError: If the requested length is less than 8.
    """
    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")

    # Build the character pool
    pool = LOWERCASE
    required_chars: list[str] = [secrets.choice(LOWERCASE)]

    if use_uppercase:
        pool += UPPERCASE
        required_chars.append(secrets.choice(UPPERCASE))

    if use_digits:
        pool += DIGITS
        required_chars.append(secrets.choice(DIGITS))

    if use_symbols:
        pool += SYMBOLS
        required_chars.append(secrets.choice(SYMBOLS))

    # Fill the remaining length with random selections from the full pool
    remaining_length = length - len(required_chars)
    password_chars = required_chars + [
        secrets.choice(pool) for _ in range(remaining_length)
    ]

    # Shuffle to avoid the guaranteed characters always being at the start
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)
