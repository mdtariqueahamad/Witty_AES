import re

with open('ui/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_css = """
        /* ============================================================
           PREMIUM DESIGN SYSTEM (Linear/1Password inspired)
           ============================================================ */
        :root {
            /* Colors - Premium Muted Palette */
            --bg-base: #0F1115;
            --bg-surface: #151922;
            --bg-surface-elevated: #1B2230;
            --bg-surface-hover: rgba(255, 255, 255, 0.04);
            
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-focus: rgba(91, 141, 239, 0.5);
            
            --text-primary: #F0F0F0;
            --text-secondary: #8A8F98;
            --text-muted: #5C616B;
            
            --accent-primary: #5B8DEF;
            --accent-primary-hover: #4A7BE0;
            
            --success: #4CAF50;
            --warning: #F5A623;
            --danger: #E85D75;
            --danger-hover: #D64A62;
            
            /* Typography */
            --font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            --font-mono: 'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, monospace;
            
            /* Spacing & Layout */
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 16px;
            
            /* Shadows (Subtle Depth) */
            --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.2);
            --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.2), 0 1px 3px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 12px 32px rgba(0, 0, 0, 0.3), 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        /* --- Global Reset --- */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: var(--font-family);
            background-color: var(--bg-base);
            color: var(--text-primary);
            height: 100vh;
            overflow: hidden;
            user-select: none;
            -webkit-user-select: none;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* --- Scrollbar --- */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: var(--border-subtle);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-muted);
        }

        /* --- Typography --- */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 600;
            letter-spacing: -0.02em;
            color: var(--text-primary);
        }

        p {
            line-height: 1.5;
            color: var(--text-secondary);
        }

        /* --- Base Layout --- */
        .app-container {
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            position: relative;
            background: var(--bg-base);
            z-index: 10;
        }

        .view {
            width: 100%;
            height: 100%;
            display: flex;
        }

        .hidden { display: none !important; }

        /* --- Subtle Surface (Replacing heavy glass) --- */
        .surface {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            box-shadow: var(--shadow-sm);
        }

        .surface-elevated {
            background: var(--bg-surface-elevated);
            border: 1px solid var(--border-subtle);
            box-shadow: var(--shadow-md);
            border-radius: var(--radius-md);
        }

        /* --- Auth Views (Login / Setup) --- */
        .auth-view {
            justify-content: center;
            align-items: center;
            background: var(--bg-base); /* Clean background */
        }

        .auth-card {
            width: 100%;
            max-width: 420px;
            padding: 40px;
            border-radius: var(--radius-lg);
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            box-shadow: var(--shadow-lg);
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .auth-icon {
            font-size: 2.5rem;
            margin-bottom: 8px;
            display: flex;
            justify-content: center;
        }
        
        /* Remove emojis visually from auth icon, replace with professional look if possible, but for now just tone it down */
        .auth-icon {
            filter: grayscale(100%) opacity(0.8);
        }

        .auth-title {
            font-size: 1.5rem;
            text-align: center;
            font-weight: 600;
        }

        .auth-subtitle {
            font-size: 0.875rem;
            text-align: center;
            color: var(--text-secondary);
            margin-top: -16px;
        }

        /* --- Form Elements --- */
        .input-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .input-label {
            font-size: 0.8125rem;
            font-weight: 500;
            color: var(--text-secondary);
        }

        .input {
            width: 100%;
            padding: 12px 14px;
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-sm);
            color: var(--text-primary);
            font-family: var(--font-family);
            font-size: 0.9375rem;
            transition: all 0.2s ease;
            outline: none;
        }

        .input:focus {
            border-color: var(--border-focus);
            box-shadow: 0 0 0 3px rgba(91, 141, 239, 0.1);
        }

        .input::placeholder {
            color: var(--text-muted);
        }

        /* --- Buttons --- */
        .btn {
            padding: 12px 20px;
            border-radius: var(--radius-sm);
            font-family: var(--font-family);
            font-size: 0.9375rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            border: none;
            outline: none;
        }

        .btn-primary {
            background: var(--accent-primary);
            color: #ffffff;
        }

        .btn-primary:hover {
            background: var(--accent-primary-hover);
            transform: translateY(-1px);
        }
        
        .btn-primary:active {
            transform: translateY(0);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-primary);
            border: 1px solid var(--border-subtle);
        }

        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.08);
        }

        .btn-danger {
            background: rgba(232, 93, 117, 0.1);
            color: var(--danger);
            border: 1px solid rgba(232, 93, 117, 0.2);
        }

        .btn-danger:hover {
            background: var(--danger);
            color: #fff;
        }

        .btn-icon {
            width: 36px;
            height: 36px;
            padding: 0;
            border-radius: var(--radius-sm);
            background: transparent;
            color: var(--text-secondary);
            border: 1px solid transparent;
        }
        
        .btn-icon:hover {
            background: var(--bg-surface-hover);
            color: var(--text-primary);
        }

        /* --- Dashboard Layout --- */
        #dashboard-view {
            display: flex;
            flex-direction: row;
        }

        /* 1. Sidebar */
        .sidebar {
            width: 260px;
            background: var(--bg-surface);
            border-right: 1px solid var(--border-subtle);
            display: flex;
            flex-direction: column;
            padding: 24px 16px;
            flex-shrink: 0;
        }

        .sidebar-header {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 0 8px;
            margin-bottom: 32px;
        }

        .logo-icon {
            width: 32px;
            height: 32px;
            background: var(--accent-primary);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            color: white;
            box-shadow: var(--shadow-sm);
        }

        .logo-text {
            font-size: 1.125rem;
            font-weight: 600;
            letter-spacing: -0.01em;
        }

        .nav-menu {
            display: flex;
            flex-direction: column;
            gap: 4px;
            flex: 1;
        }

        .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 12px;
            border-radius: var(--radius-sm);
            color: var(--text-secondary);
            font-size: 0.9375rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .nav-item:hover {
            background: var(--bg-surface-hover);
            color: var(--text-primary);
        }

        .nav-item.active {
            background: rgba(91, 141, 239, 0.1);
            color: var(--accent-primary);
        }

        .nav-icon {
            font-size: 1.1rem;
            filter: grayscale(100%);
            opacity: 0.7;
        }
        
        .nav-item.active .nav-icon {
            filter: none;
            opacity: 1;
        }

        .sidebar-footer {
            margin-top: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
            padding-top: 24px;
            border-top: 1px solid var(--border-subtle);
        }

        .vault-status {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: rgba(76, 175, 80, 0.05);
            border: 1px solid rgba(76, 175, 80, 0.1);
            border-radius: var(--radius-sm);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: var(--success);
            border-radius: 50%;
            box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
        }

        .status-text {
            font-size: 0.8125rem;
            color: var(--text-secondary);
            font-weight: 500;
        }

        /* 2. Middle Panel (List) */
        .list-panel {
            width: 340px;
            background: var(--bg-base);
            border-right: 1px solid var(--border-subtle);
            display: flex;
            flex-direction: column;
            flex-shrink: 0;
        }

        .list-header {
            padding: 24px 20px 16px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            border-bottom: 1px solid var(--border-subtle);
        }
        
        .list-header-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .list-title {
            font-size: 1.25rem;
            font-weight: 600;
        }

        .search-box {
            position: relative;
        }

        .search-icon {
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 1rem;
        }

        .search-input {
            width: 100%;
            padding: 10px 14px 10px 36px;
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-sm);
            color: var(--text-primary);
            font-size: 0.875rem;
            outline: none;
            transition: all 0.2s ease;
        }

        .search-input:focus {
            border-color: var(--border-focus);
            background: var(--bg-surface-elevated);
        }

        .cred-list {
            flex: 1;
            overflow-y: auto;
            padding: 12px 12px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .cred-card {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 12px 14px;
            border-radius: var(--radius-sm);
            cursor: pointer;
            transition: all 0.15s ease;
            border: 1px solid transparent;
        }

        .cred-card:hover {
            background: var(--bg-surface-hover);
        }

        .cred-card.selected {
            background: rgba(91, 141, 239, 0.08);
            border-color: rgba(91, 141, 239, 0.2);
        }

        .cred-avatar {
            width: 40px;
            height: 40px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.125rem;
            font-weight: 600;
            color: white;
            flex-shrink: 0;
            text-transform: uppercase;
        }

        .cred-info {
            flex: 1;
            min-width: 0;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .cred-website {
            font-size: 0.9375rem;
            font-weight: 500;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            color: var(--text-primary);
        }

        .cred-username {
            font-size: 0.8125rem;
            color: var(--text-secondary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .empty-state {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            padding: 40px;
            text-align: center;
            gap: 12px;
            color: var(--text-muted);
        }

        .empty-icon {
            font-size: 2rem;
            opacity: 0.5;
            filter: grayscale(100%);
        }

        /* 3. Detail Panel */
        .detail-panel {
            flex: 1;
            background: var(--bg-surface);
            display: flex;
            flex-direction: column;
            position: relative;
        }

        .detail-placeholder {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: var(--text-muted);
            text-align: center;
            gap: 16px;
        }

        .detail-placeholder-icon {
            font-size: 3rem;
            opacity: 0.2;
            filter: grayscale(100%);
        }
        
        .detail-placeholder-text {
            font-size: 1rem;
            font-weight: 500;
        }

        .detail-header {
            padding: 24px 32px;
            display: flex;
            justify-content: flex-end;
            gap: 8px;
            border-bottom: 1px solid var(--border-subtle);
        }

        .detail-hero {
            padding: 40px 32px 32px;
            display: flex;
            align-items: center;
            gap: 24px;
            border-bottom: 1px solid var(--border-subtle);
            background: var(--bg-base);
        }

        .detail-hero-avatar {
            width: 72px;
            height: 72px;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            font-weight: 600;
            color: white;
            text-transform: uppercase;
            box-shadow: var(--shadow-sm);
        }

        .detail-hero-info {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .detail-hero-name {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .detail-hero-category {
            font-size: 0.875rem;
            color: var(--text-secondary);
        }

        .detail-fields {
            padding: 32px;
            flex: 1;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .detail-field {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .field-label {
            font-size: 0.8125rem;
            font-weight: 500;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .field-value-container {
            display: flex;
            background: var(--bg-surface-elevated);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-sm);
            padding: 4px;
            align-items: center;
        }

        .field-value {
            flex: 1;
            padding: 10px 12px;
            font-size: 0.9375rem;
            color: var(--text-primary);
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .field-value.password {
            font-family: var(--font-mono);
            letter-spacing: 0.05em;
        }

        .field-actions {
            display: flex;
            gap: 4px;
            padding-right: 4px;
        }

        .meta-info {
            margin-top: 32px;
            padding-top: 24px;
            border-top: 1px solid var(--border-subtle);
            display: flex;
            flex-direction: column;
            gap: 8px;
            font-size: 0.8125rem;
            color: var(--text-muted);
        }

        /* --- Settings Panel --- */
        #settings-content {
            padding: 40px 32px;
            display: flex;
            flex-direction: column;
            gap: 40px;
            max-width: 800px;
            margin: 0 auto;
            width: 100%;
        }

        .settings-section {
            background: var(--bg-surface-elevated);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 32px;
        }
        
        .settings-section-header {
            margin-bottom: 24px;
            border-bottom: 1px solid var(--border-subtle);
            padding-bottom: 16px;
        }
        
        .settings-section h2 {
            font-size: 1.25rem;
            margin-bottom: 8px;
        }
        
        .settings-section p {
            font-size: 0.875rem;
        }

        /* --- Modals --- */
        .modal-overlay {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
            z-index: 100;
            display: flex;
            justify-content: center;
            align-items: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.2s ease;
        }

        .modal-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }

        .modal-card {
            width: 100%;
            max-width: 440px;
            background: var(--bg-surface-elevated);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 32px;
            box-shadow: var(--shadow-lg);
            transform: scale(0.95) translateY(10px);
            transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .modal-overlay.active .modal-card {
            transform: scale(1) translateY(0);
        }

        .modal-title {
            font-size: 1.25rem;
            font-weight: 600;
        }

        .modal-subtitle {
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-top: -12px;
        }

        .modal-actions {
            display: flex;
            justify-content: flex-end;
            gap: 12px;
            margin-top: 12px;
        }

        /* --- Components --- */
        .strength-indicator {
            height: 4px;
            background: var(--bg-surface-hover);
            border-radius: 2px;
            margin-top: 4px;
            overflow: hidden;
            display: flex;
        }
        
        .strength-bar {
            height: 100%;
            width: 0;
            transition: all 0.3s ease;
        }

        .error-msg {
            color: var(--danger);
            font-size: 0.8125rem;
            min-height: 16px;
            margin-top: 4px;
        }

        .toast-container {
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 10px;
            pointer-events: none;
        }

        .toast {
            background: var(--bg-surface-elevated);
            border: 1px solid var(--border-subtle);
            color: var(--text-primary);
            padding: 12px 20px;
            border-radius: var(--radius-sm);
            font-size: 0.875rem;
            font-weight: 500;
            box-shadow: var(--shadow-md);
            display: flex;
            align-items: center;
            gap: 12px;
            animation: toastIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        .toast.success { border-left: 3px solid var(--success); }
        .toast.error { border-left: 3px solid var(--danger); }
        .toast.info { border-left: 3px solid var(--accent-primary); }

        @keyframes toastIn {
            from { opacity: 0; transform: translateY(20px) scale(0.95); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }

        @keyframes toastOut {
            from { opacity: 1; transform: translateY(0) scale(1); }
            to { opacity: 0; transform: translateY(10px) scale(0.95); }
        }

        .spinner {
            width: 16px;
            height: 16px;
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-top-color: currentColor;
            border-radius: 50%;
            animation: spin 0.6s linear infinite;
            display: inline-block;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .password-dots { font-family: var(--font-mono); letter-spacing: 0.15em; }

        /* Premium Avatar Color Palette (Muted, elegant) */
        .avatar-0 { background: #E57373; }
        .avatar-1 { background: #F06292; }
        .avatar-2 { background: #BA68C8; }
        .avatar-3 { background: #7986CB; }
        .avatar-4 { background: #64B5F6; }
        .avatar-5 { background: #4DD0E1; }
        .avatar-6 { background: #4DB6AC; }
        .avatar-7 { background: #81C784; }
        .avatar-8 { background: #AED581; }
        .avatar-9 { background: #FFB74D; }
"""

# Extract the style block and replace it
style_pattern = re.compile(r'<style>.*?</style>', re.DOTALL)
content = style_pattern.sub(f'<style>\n{new_css}\n    </style>', content)

# Remove the animated-bg div
content = re.sub(r'<!-- Animated gradient background -->\s*<div class="animated-bg"></div>', '', content)

# Remove the watermark
content = re.sub(r'<!-- Branding Watermark -->\s*<div class="watermark">\s*Secured by <strong>WittyArtist</strong>\s*</div>', '', content)

# Remove the glass class where it exists since we use surface classes now
content = content.replace('auth-card glass', 'auth-card')
content = content.replace('modal-card glass', 'modal-card')
content = content.replace('glass-hover', '')

with open('ui/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
