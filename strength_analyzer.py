"""
strength_analyzer.py — Local password strength evaluation engine.

Grades each password as "Strong", "Good", or "Weak" based on:
  - Length thresholds
  - Character class diversity (uppercase, lowercase, digits, symbols)
  - Penalty for common weak patterns (sequential chars, repeated chars)

No network requests — all analysis is done locally.
"""

import re


# ---------------------------------------------------------------------------
# Strength Grading
# ---------------------------------------------------------------------------
def analyze_strength(password: str) -> str:
    """
    Evaluate a single password's strength.

    Scoring system:
      - Base score from length
      - Bonus for character class diversity
      - Penalty for weak patterns

    Args:
        password: The plaintext password to evaluate.

    Returns:
        "Strong", "Good", or "Weak".
    """
    if not password:
        return "Weak"

    score = 0
    length = len(password)

    # --- Length scoring ---
    if length >= 20:
        score += 4
    elif length >= 16:
        score += 3
    elif length >= 12:
        score += 2
    elif length >= 8:
        score += 1
    # < 8 gets 0

    # --- Character diversity ---
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_symbol = bool(re.search(r'[^A-Za-z0-9]', password))

    diversity = sum([has_lower, has_upper, has_digit, has_symbol])
    score += diversity  # 0-4 points

    # --- Penalty: all same character ---
    if len(set(password)) == 1:
        score -= 3

    # --- Penalty: sequential patterns (abc, 123, etc.) ---
    sequential_count = 0
    for i in range(len(password) - 2):
        if (ord(password[i]) + 1 == ord(password[i + 1]) == ord(password[i + 2]) - 1):
            sequential_count += 1
    if sequential_count >= 2:
        score -= 1

    # --- Penalty: repeated characters (aaa, 111) ---
    repeat_count = 0
    for i in range(len(password) - 2):
        if password[i] == password[i + 1] == password[i + 2]:
            repeat_count += 1
    if repeat_count >= 2:
        score -= 1

    # --- Penalty: too short is always weak ---
    if length < 8:
        return "Weak"

    # --- Final grading ---
    if score >= 6:
        return "Strong"
    elif score >= 4:
        return "Good"
    else:
        return "Weak"


def analyze_all(credentials: list[dict]) -> dict:
    """
    Analyze a list of credentials and group them by strength.

    Args:
        credentials: A list of dicts, each containing at least
                     'id', 'website', 'username', and 'password' keys.

    Returns:
        A dict with keys 'strong', 'good', 'weak', each containing
        a list of credential dicts with an added 'strength' field.
    """
    result = {"strong": [], "good": [], "weak": []}

    for cred in credentials:
        password = cred.get("password", "")
        strength = analyze_strength(password)
        entry = {
            "id": cred.get("id"),
            "website": cred.get("website", ""),
            "username": cred.get("username", ""),
            "strength": strength,
            "password_length": len(password),
        }

        if strength == "Strong":
            result["strong"].append(entry)
        elif strength == "Good":
            result["good"].append(entry)
        else:
            result["weak"].append(entry)

    return result
