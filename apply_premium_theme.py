import re

with open('/Users/mdtariqueahamad/Project/Password Manager/ui/index.html', 'r') as f:
    html = f.read()

# 1. Update the CSS Variables
new_vars = """
        :root {
            /* Premium Dark Theme Colors */
            --bg-base: #0F1115;
            --bg-panel: #151922;
            --bg-sidebar: #151922;
            
            --glass-bg: rgba(255, 255, 255, 0.04);
            --glass-bg-hover: rgba(255, 255, 255, 0.06);
            --glass-border: rgba(255, 255, 255, 0.08);
            --glass-border-hover: rgba(255, 255, 255, 0.12);
            --glass-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
            --glass-blur: 8px; /* Subtle blur */

            --text-primary: #FFFFFF;
            --text-secondary: #8A8F98;
            --text-muted: #5C616B;

            --accent-primary: #5B8DEF;
            --accent-primary-hover: #4A7BE0;
            --accent-danger: #E85D75;
            --accent-success: #4CAF50;
            --accent-warning: #F5A623;

            /* Typography */
            --font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 16px;
        }
"""
html = re.sub(r':root\s*\{[^}]+\}', new_vars, html)

# 2. Remove the animated-bg completely and make background solid
html = re.sub(r'\.animated-bg.*?(?=\.glass \{)', """
        body {
            background-color: var(--bg-base);
        }
        .animated-bg { display: none; }
""", html, flags=re.DOTALL)

# 3. Mute the Avatar Colors
avatar_colors = """
        /* Premium Avatar Color Palette */
        .avatar-0 { background: #E57373; }
        .avatar-1 { background: #F06292; }
        .avatar-2 { background: #BA68C8; }
        .avatar-3 { background: #7986CB; }
        .avatar-4 { background: #64B5F6; }
        .avatar-5 { background: #4DD0E1; }
        .avatar-6 { background: #4DB6AC; }
        .avatar-7 { background: #81C784; }
"""
html = re.sub(r'/\* Avatar Color Palette \*/.*?(?=</style>)', avatar_colors, html, flags=re.DOTALL)

# 4. Remove Cybersecurity Emojis & Neon texts from HTML
html = html.replace('<div class="auth-icon">🛡️</div>', '<div class="auth-icon" style="font-size: 2rem; color: var(--accent-primary);">✧</div>')
html = html.replace('<div class="auth-icon">🔐</div>', '<div class="auth-icon" style="font-size: 2rem; color: var(--accent-primary);">✧</div>')
html = html.replace('<div class="logo-icon">🔒</div>', '<div class="logo-icon" style="background: transparent; border: 1px solid var(--glass-border); font-size: 1rem;">✧</div>')
html = html.replace('🔒&nbsp; Create Vault', 'Create Vault')
html = html.replace('🔓&nbsp; Unlock', 'Unlock')
html = html.replace('⚡ Generate', 'Generate')
html = html.replace('＋ Add New Credential', 'Add New Credential')

# 5. Clean up specific CSS classes that had glows/shadows
html = html.replace('text-shadow: 0 0 20px rgba(124, 58, 237, 0.4);', '')
html = html.replace('box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);', '')

with open('/Users/mdtariqueahamad/Project/Password Manager/ui/index.html', 'w') as f:
    f.write(html)
