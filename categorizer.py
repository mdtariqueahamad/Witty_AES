"""
categorizer.py — Lightweight offline auto-categorization engine.

Uses a keyword-matching dictionary heuristic to assign categories to
credentials based on their website/service name. No network requests,
no ML — just fast string matching.

If the user provides a category manually, that takes precedence.
This module is only used when the category field is left blank.
"""


# ---------------------------------------------------------------------------
# Category Rules — keyword lists for each category
# ---------------------------------------------------------------------------
CATEGORY_RULES: dict[str, list[str]] = {
    "Social": [
        "facebook", "instagram", "twitter", "x.com", "tiktok", "snapchat",
        "reddit", "linkedin", "pinterest", "tumblr", "discord", "whatsapp",
        "telegram", "mastodon", "threads", "signal", "wechat", "line",
        "viber", "kik", "clubhouse", "meetup",
    ],
    "Finance": [
        "bank", "hdfc", "icici", "sbi", "chase", "paypal", "razorpay",
        "stripe", "gpay", "paytm", "phonepe", "wise", "revolut", "venmo",
        "capital one", "capitalone", "wells fargo", "wellsfargo", "citi",
        "barclays", "hsbc", "axis", "kotak", "bajaj", "groww", "zerodha",
        "upstox", "kite", "angel", "fidelity", "schwab", "robinhood",
        "coinbase", "binance", "crypto", "wallet",
    ],
    "Work": [
        "github", "gitlab", "bitbucket", "jira", "confluence", "slack",
        "notion", "figma", "vercel", "netlify", "heroku", "aws", "azure",
        "gcp", "docker", "trello", "asana", "linear", "stackoverflow",
        "codepen", "replit", "codesandbox", "jetbrains", "vscode",
        "postman", "swagger", "kubernetes", "jenkins", "circleci",
        "datadog", "grafana", "sentry", "pagerduty", "zoom", "teams",
        "webex", "salesforce", "hubspot", "freshdesk",
    ],
    "Shopping": [
        "amazon", "flipkart", "ebay", "walmart", "shopify", "myntra",
        "ajio", "zara", "nike", "adidas", "etsy", "aliexpress", "wish",
        "target", "bestbuy", "swiggy", "zomato", "uber eats", "ubereats",
        "doordash", "instacart", "bigbasket", "blinkit", "meesho",
        "nykaa", "tatacliq",
    ],
    "Email": [
        "gmail", "outlook", "hotmail", "yahoo", "proton", "protonmail",
        "zoho", "mail", "icloud", "fastmail", "tutanota", "aol",
        "yandex", "mailchimp", "sendgrid",
    ],
    "Entertainment": [
        "netflix", "spotify", "youtube", "disney", "disneyplus", "hulu",
        "hbo", "prime video", "primevideo", "apple tv", "appletv",
        "crunchyroll", "twitch", "steam", "epic games", "epicgames",
        "playstation", "xbox", "nintendo", "ea", "ubisoft", "riot",
        "valorant", "minecraft", "roblox", "audible", "kindle",
        "hotstar", "jiocinema", "sonyliv", "zee5", "voot", "mxplayer",
    ],
    "Education": [
        "coursera", "udemy", "edx", "khan academy", "khanacademy",
        "skillshare", "pluralsight", "linkedin learning", "codecademy",
        "freecodecamp", "leetcode", "hackerrank", "codechef", "codeforces",
        "brilliant", "duolingo", "byjus", "unacademy", "vedantu",
    ],
}


def auto_categorize(website: str) -> str:
    """
    Auto-assign a category based on the website/service name.

    Performs case-insensitive substring matching against a curated
    dictionary of known services.

    Args:
        website: The website or service name to categorize.

    Returns:
        A category string (e.g., "Social", "Finance") or "Other"
        if no match is found.
    """
    website_lower = website.lower().strip()

    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword in website_lower:
                return category

    return "Other"


def get_all_categories() -> list[str]:
    """Return a sorted list of all known category names including 'Other'."""
    return sorted(CATEGORY_RULES.keys()) + ["Other"]
