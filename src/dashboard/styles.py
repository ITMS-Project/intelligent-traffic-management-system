"""
🎨 PREMIUM FUTURISTIC UI STYLES
Intelligent Traffic Management System
Inspired by cyberpunk/AI aesthetics with glassmorphism and animations
"""

# ============================================================================
# 🎨 COLOR PALETTE
# ============================================================================
COLORS = {
    # Primary Dark Theme
    "bg_primary": "#0a0a0a",
    "bg_secondary": "#111111",
    "bg_tertiary": "#1a1a1a",
    "bg_card": "rgba(20, 20, 20, 0.8)",
    
    # Accent Colors
    "accent_primary": "#00ff88",      # Neon Green
    "accent_secondary": "#00d4ff",    # Cyan
    "accent_warning": "#ffaa00",      # Amber
    "accent_danger": "#ff4757",       # Red
    "accent_success": "#2ed573",      # Green
    
    # Text Colors
    "text_primary": "#ffffff",
    "text_secondary": "#a0a0a0",
    "text_muted": "#666666",
    
    # Glass Effects
    "glass_bg": "rgba(255, 255, 255, 0.03)",
    "glass_border": "rgba(255, 255, 255, 0.08)",
    "glass_highlight": "rgba(255, 255, 255, 0.1)",
}

# ============================================================================
# 🎬 AUTHORITY DASHBOARD STYLES (Futuristic Command Center)
# ============================================================================
DASHBOARD_CSS = """
<style>
    /* ========================================
       🌐 GOOGLE FONTS IMPORT
       ======================================== */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ========================================
       🎨 CSS VARIABLES
       ======================================== */
    :root {
        --bg-primary: #050505;
        --bg-secondary: #0a0a0a;
        --bg-tertiary: #111111;
        --bg-card: rgba(15, 15, 15, 0.9);
        
        --accent-green: #00ff88;
        --accent-cyan: #00d4ff;
        --accent-amber: #ffaa00;
        --accent-red: #ff4757;
        --accent-purple: #a855f7;
        
        --text-primary: #ffffff;
        --text-secondary: #b0b0b0;
        --text-muted: #555555;
        
        --glass-bg: rgba(255, 255, 255, 0.02);
        --glass-border: rgba(255, 255, 255, 0.06);
        
        --font-display: 'Orbitron', sans-serif;
        --font-heading: 'Rajdhani', sans-serif;
        --font-body: 'Space Grotesk', sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
        
        --transition-fast: 0.15s ease;
        --transition-normal: 0.3s ease;
        --transition-slow: 0.5s ease;
    }

    /* ========================================
       🌌 GLOBAL STYLES & BACKGROUND
       ======================================== */
    .stApp {
        background: var(--bg-primary);
        background-image: 
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(0, 255, 136, 0.08), transparent),
            radial-gradient(ellipse 60% 40% at 100% 50%, rgba(0, 212, 255, 0.05), transparent),
            radial-gradient(ellipse 50% 30% at 0% 80%, rgba(168, 85, 247, 0.05), transparent);
        min-height: 100vh;
        font-family: var(--font-body);
        color: var(--text-primary);
    }

    /* Animated Mesh Background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
        background-size: 60px 60px;
        pointer-events: none;
        z-index: 0;
        animation: meshMove 30s linear infinite;
    }

    @keyframes meshMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(60px, 60px); }
    }

    /* Floating Particles Effect */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(1px 1px at 20% 30%, rgba(0, 255, 136, 0.3), transparent),
            radial-gradient(1px 1px at 40% 70%, rgba(0, 212, 255, 0.3), transparent),
            radial-gradient(1px 1px at 60% 20%, rgba(255, 255, 255, 0.2), transparent),
            radial-gradient(1px 1px at 80% 60%, rgba(0, 255, 136, 0.2), transparent);
        background-size: 200px 200px;
        pointer-events: none;
        z-index: 0;
        animation: particleFloat 20s ease-in-out infinite;
        opacity: 0.6;
    }

    @keyframes particleFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }

    /* ========================================
       🎯 MAIN HEADER
       ======================================== */
    .main-header {
        background: linear-gradient(135deg, rgba(10, 10, 10, 0.95), rgba(20, 20, 20, 0.9));
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        overflow: hidden;
        animation: slideDown 0.6s ease-out;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--accent-green), var(--accent-cyan), transparent);
        animation: headerGlow 3s ease-in-out infinite;
    }

    @keyframes headerGlow {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }

    .header-title {
        font-family: var(--font-display);
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: 4px;
        background: linear-gradient(135deg, #fff 0%, var(--accent-green) 50%, var(--accent-cyan) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-transform: uppercase;
        position: relative;
    }

    .header-subtitle {
        font-family: var(--font-mono);
        font-size: 0.75rem;
        color: var(--accent-green);
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 0.25rem;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 0.7; }
        50% { opacity: 1; }
    }

    /* ========================================
       🎴 GLASSMORPHISM CARDS
       ======================================== */
    .glass-card {
        background: linear-gradient(135deg, rgba(20, 20, 20, 0.9), rgba(10, 10, 10, 0.95));
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
        transition: all var(--transition-normal);
        animation: fadeInUp 0.5s ease-out;
    }

    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03), transparent);
        pointer-events: none;
    }

    .glass-card:hover {
        border-color: rgba(0, 255, 136, 0.2);
        transform: translateY(-4px);
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.4),
            0 0 40px rgba(0, 255, 136, 0.1);
    }

    /* Stat Cards */
    .stat-card {
        background: linear-gradient(145deg, rgba(15, 15, 15, 0.95), rgba(5, 5, 5, 0.98));
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        position: relative;
        overflow: hidden;
        transition: all var(--transition-normal);
    }

    .stat-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, var(--accent-green), var(--accent-cyan));
        border-radius: 4px 0 0 4px;
    }

    .stat-card:hover {
        transform: scale(1.02);
        border-color: rgba(0, 255, 136, 0.3);
    }

    .stat-value {
        font-family: var(--font-display);
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
        margin-bottom: 0.5rem;
    }

    .stat-label {
        font-family: var(--font-body);
        font-size: 0.85rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stat-delta {
        font-family: var(--font-mono);
        font-size: 0.75rem;
        padding: 0.25rem 0.5rem;
        border-radius: 6px;
        display: inline-block;
        margin-top: 0.5rem;
    }

    .stat-delta.positive {
        background: rgba(0, 255, 136, 0.15);
        color: var(--accent-green);
    }

    .stat-delta.negative {
        background: rgba(255, 71, 87, 0.15);
        color: var(--accent-red);
    }

    /* ========================================
       📊 STREAMLIT METRIC OVERRIDE
       ======================================== */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(15, 15, 15, 0.95), rgba(5, 5, 5, 0.98));
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1.25rem;
        position: relative;
        overflow: hidden;
        transition: all var(--transition-normal);
    }

    div[data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-green), var(--accent-cyan), var(--accent-purple));
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 255, 136, 0.2);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    div[data-testid="stMetricLabel"] {
        font-family: var(--font-body);
        font-size: 0.8rem !important;
        color: var(--text-secondary) !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    div[data-testid="stMetricValue"] {
        font-family: var(--font-display) !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
    }

    div[data-testid="stMetricDelta"] {
        font-family: var(--font-mono);
        font-size: 0.85rem !important;
    }

    div[data-testid="stMetricDelta"] svg {
        display: none;
    }

    /* ========================================
       🔘 BUTTONS
       ======================================== */
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 212, 255, 0.1));
        color: var(--text-primary);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 50px;
        padding: 0.75rem 2rem;
        font-family: var(--font-body);
        font-weight: 600;
        font-size: 0.9rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: all var(--transition-normal);
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, var(--accent-green), var(--accent-cyan));
        color: #000;
        border-color: var(--accent-green);
        transform: translateY(-2px);
        box-shadow: 
            0 10px 30px rgba(0, 255, 136, 0.3),
            0 0 60px rgba(0, 255, 136, 0.2);
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Primary CTA Button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--accent-green), var(--accent-cyan));
        color: #000;
        font-weight: 700;
        box-shadow: 0 5px 20px rgba(0, 255, 136, 0.3);
    }

    .stButton > button[kind="primary"]:hover {
        box-shadow: 
            0 15px 40px rgba(0, 255, 136, 0.4),
            0 0 80px rgba(0, 255, 136, 0.3);
    }

    /* ========================================
       📝 INPUT FIELDS
       ======================================== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(10, 10, 10, 0.8);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        color: var(--text-primary);
        font-family: var(--font-body);
        padding: 0.75rem 1rem;
        transition: all var(--transition-normal);
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-green);
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.15);
        outline: none;
    }

    .stTextInput > label,
    .stNumberInput > label,
    .stTextArea > label,
    .stSelectbox > label {
        font-family: var(--font-body);
        font-size: 0.85rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ========================================
       📋 SELECT BOXES & DROPDOWNS
       ======================================== */
    .stSelectbox > div > div {
        background: rgba(10, 10, 10, 0.8);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        transition: all var(--transition-normal);
    }

    .stSelectbox > div > div:hover {
        border-color: rgba(0, 255, 136, 0.3);
    }

    /* ========================================
       🗂️ TABS
       ======================================== */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(10, 10, 10, 0.6);
        border-radius: 16px;
        padding: 0.5rem;
        gap: 0.5rem;
        border: 1px solid var(--glass-border);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: var(--text-secondary);
        font-family: var(--font-body);
        font-weight: 500;
        font-size: 0.9rem;
        padding: 0.75rem 1.5rem;
        border: none;
        transition: all var(--transition-normal);
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text-primary);
        background: rgba(255, 255, 255, 0.05);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(0, 212, 255, 0.2));
        color: var(--accent-green);
        border: 1px solid rgba(0, 255, 136, 0.3);
    }

    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }

    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* ========================================
       📊 DATAFRAMES & TABLES
       ======================================== */
    .stDataFrame {
        background: rgba(10, 10, 10, 0.8);
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid var(--glass-border);
    }

    .stDataFrame [data-testid="stDataFrameResizable"] {
        background: transparent;
    }

    .stDataFrame table {
        font-family: var(--font-body);
    }

    .stDataFrame thead tr th {
        background: rgba(0, 255, 136, 0.1);
        color: var(--accent-green);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.8rem;
    }

    .stDataFrame tbody tr {
        transition: background var(--transition-fast);
    }

    .stDataFrame tbody tr:hover {
        background: rgba(0, 255, 136, 0.05);
    }

    /* ========================================
       📈 PLOTLY CHARTS
       ======================================== */
    .js-plotly-plot {
        border-radius: 16px;
        overflow: hidden;
    }

    /* ========================================
       🎬 VIDEO CONTAINER
       ======================================== */
    .video-container {
        position: relative;
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid var(--glass-border);
        background: rgba(10, 10, 10, 0.8);
    }

    .video-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border: 2px solid transparent;
        border-radius: 20px;
        background: linear-gradient(135deg, var(--accent-green), var(--accent-cyan)) border-box;
        -webkit-mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
        mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: destination-out;
        mask-composite: exclude;
        pointer-events: none;
        opacity: 0;
        transition: opacity var(--transition-normal);
    }

    .video-container:hover::before {
        opacity: 0.5;
    }

    /* HUD Corners */
    .hud-corner {
        position: absolute;
        width: 30px;
        height: 30px;
        border: 2px solid var(--accent-green);
        z-index: 10;
        pointer-events: none;
    }

    .hud-corner.top-left { top: 15px; left: 15px; border-right: 0; border-bottom: 0; }
    .hud-corner.top-right { top: 15px; right: 15px; border-left: 0; border-bottom: 0; }
    .hud-corner.bottom-left { bottom: 15px; left: 15px; border-right: 0; border-top: 0; }
    .hud-corner.bottom-right { bottom: 15px; right: 15px; border-left: 0; border-top: 0; }

    /* ========================================
       📊 SIDEBAR
       ======================================== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(5, 5, 5, 0.98), rgba(10, 10, 10, 0.95));
        border-right: 1px solid var(--glass-border);
    }

    section[data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            linear-gradient(rgba(0, 255, 136, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 136, 0.02) 1px, transparent 1px);
        background-size: 30px 30px;
        pointer-events: none;
    }

    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        font-family: var(--font-heading);
        color: var(--accent-green);
    }

    /* ========================================
       📝 FILE UPLOADER
       ======================================== */
    .stFileUploader {
        background: rgba(10, 10, 10, 0.6);
        border: 2px dashed var(--glass-border);
        border-radius: 16px;
        transition: all var(--transition-normal);
    }

    .stFileUploader:hover {
        border-color: var(--accent-green);
        background: rgba(0, 255, 136, 0.02);
    }

    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        background: transparent;
    }

    /* ========================================
       ⏳ PROGRESS BAR
       ======================================== */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--accent-green), var(--accent-cyan));
        border-radius: 10px;
        height: 8px;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
    }

    .stProgress > div > div {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }

    /* ========================================
       💬 ALERTS & NOTIFICATIONS
       ======================================== */
    .stAlert {
        background: rgba(10, 10, 10, 0.9);
        border-radius: 12px;
        border: 1px solid;
        backdrop-filter: blur(10px);
    }

    .stAlert[data-baseweb="notification"] {
        font-family: var(--font-body);
    }

    /* Info Alert */
    div[data-testid="stAlert"][data-type="info"] {
        background: rgba(0, 212, 255, 0.1);
        border-color: rgba(0, 212, 255, 0.3);
    }

    /* Success Alert */
    div[data-testid="stAlert"][data-type="success"] {
        background: rgba(0, 255, 136, 0.1);
        border-color: rgba(0, 255, 136, 0.3);
    }

    /* Warning Alert */
    div[data-testid="stAlert"][data-type="warning"] {
        background: rgba(255, 170, 0, 0.1);
        border-color: rgba(255, 170, 0, 0.3);
    }

    /* Error Alert */
    div[data-testid="stAlert"][data-type="error"] {
        background: rgba(255, 71, 87, 0.1);
        border-color: rgba(255, 71, 87, 0.3);
    }

    /* ========================================
       🎯 STATUS BADGES
       ======================================== */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 1rem;
        border-radius: 50px;
        font-family: var(--font-mono);
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .status-badge.online {
        background: rgba(0, 255, 136, 0.15);
        color: var(--accent-green);
        border: 1px solid rgba(0, 255, 136, 0.3);
    }

    .status-badge.online::before {
        content: '';
        width: 8px;
        height: 8px;
        background: var(--accent-green);
        border-radius: 50%;
        animation: statusPulse 2s ease-in-out infinite;
    }

    .status-badge.warning {
        background: rgba(255, 170, 0, 0.15);
        color: var(--accent-amber);
        border: 1px solid rgba(255, 170, 0, 0.3);
    }

    .status-badge.danger {
        background: rgba(255, 71, 87, 0.15);
        color: var(--accent-red);
        border: 1px solid rgba(255, 71, 87, 0.3);
    }

    @keyframes statusPulse {
        0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.5); }
        50% { opacity: 0.7; box-shadow: 0 0 0 8px rgba(0, 255, 136, 0); }
    }

    /* ========================================
       🎬 ANIMATIONS
       ======================================== */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes fadeInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    @keyframes glowPulse {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 136, 0.3); }
        50% { box-shadow: 0 0 40px rgba(0, 255, 136, 0.5); }
    }

    /* Staggered animation delays */
    .animate-1 { animation-delay: 0.1s; }
    .animate-2 { animation-delay: 0.2s; }
    .animate-3 { animation-delay: 0.3s; }
    .animate-4 { animation-delay: 0.4s; }
    .animate-5 { animation-delay: 0.5s; }

    /* ========================================
       🎨 SPECIAL ELEMENTS
       ======================================== */
    
    /* Hero Text (Outline Style) */
    .hero-text {
        font-family: var(--font-display);
        font-size: 4rem;
        font-weight: 900;
        color: transparent;
        -webkit-text-stroke: 2px var(--text-primary);
        text-transform: uppercase;
        letter-spacing: 4px;
        line-height: 1.1;
    }

    .hero-text span {
        color: var(--text-primary);
        -webkit-text-stroke: 0;
    }

    /* Live Indicator */
    .live-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(255, 71, 87, 0.15);
        border: 1px solid rgba(255, 71, 87, 0.3);
        border-radius: 50px;
        font-family: var(--font-mono);
        font-size: 0.8rem;
        color: var(--accent-red);
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .live-indicator::before {
        content: '';
        width: 10px;
        height: 10px;
        background: var(--accent-red);
        border-radius: 50%;
        animation: livePulse 1.5s ease-in-out infinite;
    }

    @keyframes livePulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
    }

    /* Divider */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--glass-border), transparent);
        margin: 2rem 0;
    }

    /* ========================================
       📱 RESPONSIVE DESIGN
       ======================================== */
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem;
            flex-direction: column;
            gap: 1rem;
        }

        .header-title {
            font-size: 1.2rem;
        }

        .hero-text {
            font-size: 2rem;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
    }

    /* ========================================
       🔧 UTILITY CLASSES
       ======================================== */
    .text-gradient {
        background: linear-gradient(135deg, var(--accent-green), var(--accent-cyan));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .glow-green {
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
    }

    .glow-cyan {
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    }

    .border-glow {
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.2);
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

</style>
"""


# ============================================================================
# 📱 MOBILE DRIVER APP STYLES (Premium Automotive Design)
# ============================================================================
MOBILE_CSS = """
<style>
    /* ========================================
       🌐 GOOGLE FONTS IMPORT
       ======================================== */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ========================================
       🎨 CSS VARIABLES
       ======================================== */
    :root {
        --bg-primary: #000000;
        --bg-secondary: #0a0a0a;
        --bg-card: rgba(12, 12, 12, 0.95);
        
        --accent-green: #00ff88;
        --accent-cyan: #00d4ff;
        --accent-blue: #2563eb;
        --accent-purple: #8b5cf6;
        --accent-amber: #f59e0b;
        --accent-red: #ef4444;
        
        --text-primary: #ffffff;
        --text-secondary: #9ca3af;
        --text-muted: #4b5563;
        
        --glass-bg: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.08);
        
        --font-display: 'Orbitron', sans-serif;
        --font-heading: 'Rajdhani', sans-serif;
        --font-body: 'Space Grotesk', sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
    }

    /* ========================================
       🌌 GLOBAL STYLES
       ======================================== */
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #050510 50%, #0a0a15 100%);
        min-height: 100vh;
        font-family: var(--font-body);
        color: var(--text-primary);
        position: relative;
    }

    /* Subtle gradient orbs */
    .stApp::before {
        content: '';
        position: fixed;
        top: -20%;
        right: -20%;
        width: 60%;
        height: 60%;
        background: radial-gradient(circle, rgba(0, 255, 136, 0.08) 0%, transparent 60%);
        pointer-events: none;
        z-index: 0;
    }

    .stApp::after {
        content: '';
        position: fixed;
        bottom: -20%;
        left: -20%;
        width: 60%;
        height: 60%;
        background: radial-gradient(circle, rgba(0, 212, 255, 0.06) 0%, transparent 60%);
        pointer-events: none;
        z-index: 0;
    }

    /* ========================================
       🎯 APP HEADER
       ======================================== */
    .app-header {
        text-align: center;
        padding: 2rem 1rem;
        position: relative;
    }

    .app-logo {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, var(--accent-green), var(--accent-cyan));
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        font-family: var(--font-display);
        font-size: 1.5rem;
        font-weight: 700;
        color: #000;
        box-shadow: 0 10px 40px rgba(0, 255, 136, 0.3);
    }

    .app-title {
        font-family: var(--font-display);
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: 3px;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }

    .app-subtitle {
        font-family: var(--font-mono);
        font-size: 0.75rem;
        color: var(--accent-green);
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* ========================================
       🏆 SAFETY SCORE CARD
       ======================================== */
    .score-card {
        background: linear-gradient(145deg, rgba(15, 15, 20, 0.95), rgba(5, 5, 10, 0.98));
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        margin-bottom: 1.5rem;
    }

    .score-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--accent-green), var(--accent-cyan), transparent);
        border-radius: 0 0 10px 10px;
    }

    .score-circle {
        width: 160px;
        height: 160px;
        border-radius: 50%;
        background: conic-gradient(
            var(--accent-green) calc(var(--score) * 3.6deg),
            rgba(255, 255, 255, 0.05) 0deg
        );
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        position: relative;
        box-shadow: 
            0 0 40px rgba(0, 255, 136, 0.2),
            inset 0 0 30px rgba(0, 0, 0, 0.5);
    }

    .score-circle::before {
        content: '';
        position: absolute;
        width: 130px;
        height: 130px;
        background: linear-gradient(145deg, #0a0a0f, #050508);
        border-radius: 50%;
    }

    .score-value {
        position: relative;
        z-index: 1;
        font-family: var(--font-display);
        font-size: 3rem;
        font-weight: 700;
        color: var(--text-primary);
        text-shadow: 0 0 30px rgba(0, 255, 136, 0.5);
    }

    .score-label {
        font-family: var(--font-body);
        font-size: 0.9rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .score-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1.25rem;
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 50px;
        font-family: var(--font-mono);
        font-size: 0.8rem;
        color: var(--accent-green);
        margin-top: 1rem;
    }

    /* ========================================
       📋 VIOLATION CARD
       ======================================== */
    .violation-card {
        background: linear-gradient(145deg, rgba(15, 15, 20, 0.95), rgba(8, 8, 12, 0.98));
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .violation-card::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: linear-gradient(180deg, var(--accent-red), var(--accent-amber));
        border-radius: 4px 0 0 4px;
    }

    .violation-card:hover {
        transform: translateX(4px);
        border-color: rgba(255, 71, 87, 0.3);
    }

    .violation-card.paid::before {
        background: linear-gradient(180deg, var(--accent-green), var(--accent-cyan));
    }

    .violation-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 0.75rem;
    }

    .violation-type {
        font-family: var(--font-heading);
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
    }

    .violation-status {
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-family: var(--font-mono);
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .violation-status.pending {
        background: rgba(255, 71, 87, 0.15);
        color: var(--accent-red);
        border: 1px solid rgba(255, 71, 87, 0.3);
    }

    .violation-status.paid {
        background: rgba(0, 255, 136, 0.15);
        color: var(--accent-green);
        border: 1px solid rgba(0, 255, 136, 0.3);
    }

    .violation-details {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
        margin-bottom: 0.75rem;
    }

    .violation-detail {
        font-family: var(--font-body);
        font-size: 0.8rem;
        color: var(--text-secondary);
    }

    .violation-detail span {
        color: var(--text-primary);
        font-weight: 500;
    }

    .violation-fine {
        font-family: var(--font-display);
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--accent-amber);
        text-align: right;
    }

    /* ========================================
       🚗 VEHICLE CARD
       ======================================== */
    .vehicle-card {
        background: linear-gradient(145deg, rgba(15, 15, 20, 0.95), rgba(8, 8, 12, 0.98));
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        position: relative;
        transition: all 0.3s ease;
    }

    .vehicle-card:hover {
        border-color: rgba(0, 212, 255, 0.3);
        transform: translateY(-2px);
    }

    .vehicle-plate {
        font-family: var(--font-display);
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        padding: 0.5rem 1rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--glass-border);
        border-radius: 8px;
        display: inline-block;
        margin-bottom: 1rem;
        letter-spacing: 2px;
    }

    .vehicle-info {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
    }

    .vehicle-info-item {
        font-family: var(--font-body);
        font-size: 0.85rem;
        color: var(--text-secondary);
    }

    .vehicle-info-item strong {
        color: var(--text-primary);
        display: block;
        margin-bottom: 0.25rem;
    }

    /* ========================================
       ⚠️ WARNING BANNER
       ======================================== */
    .warning-banner {
        background: linear-gradient(135deg, rgba(255, 71, 87, 0.15), rgba(255, 170, 0, 0.1));
        border: 1px solid rgba(255, 71, 87, 0.3);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        animation: warningPulse 3s ease-in-out infinite;
    }

    @keyframes warningPulse {
        0%, 100% { box-shadow: 0 0 20px rgba(255, 71, 87, 0.2); }
        50% { box-shadow: 0 0 40px rgba(255, 71, 87, 0.4); }
    }

    .warning-banner::before {
        content: '⚠️';
        position: absolute;
        top: 50%;
        right: 1rem;
        transform: translateY(-50%);
        font-size: 2rem;
        opacity: 0.3;
    }

    .warning-title {
        font-family: var(--font-heading);
        font-size: 1rem;
        font-weight: 700;
        color: var(--accent-red);
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .warning-message {
        font-family: var(--font-body);
        font-size: 0.9rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }

    /* ========================================
       💳 PAYMENT SECTION
       ======================================== */
    .payment-card {
        background: linear-gradient(145deg, rgba(15, 15, 20, 0.95), rgba(8, 8, 12, 0.98));
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .payment-amount {
        text-align: center;
        margin-bottom: 1.5rem;
    }

    .payment-amount-label {
        font-family: var(--font-body);
        font-size: 0.85rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }

    .payment-amount-value {
        font-family: var(--font-display);
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
    }

    .payment-amount-value span {
        font-size: 1.25rem;
        color: var(--text-secondary);
    }

    .payment-methods {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }

    .payment-method {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .payment-method:hover {
        border-color: var(--accent-cyan);
        background: rgba(0, 212, 255, 0.05);
    }

    .payment-method.selected {
        border-color: var(--accent-green);
        background: rgba(0, 255, 136, 0.1);
    }

    .payment-method-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }

    .payment-method-name {
        font-family: var(--font-body);
        font-size: 0.8rem;
        color: var(--text-secondary);
    }

    /* ========================================
       🔘 BUTTONS (MOBILE)
       ======================================== */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-green), var(--accent-cyan));
        color: #000;
        border: none;
        border-radius: 14px;
        padding: 1rem 2rem;
        font-family: var(--font-body);
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 8px 30px rgba(0, 255, 136, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 
            0 12px 40px rgba(0, 255, 136, 0.4),
            0 0 60px rgba(0, 255, 136, 0.2);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Secondary Button Style */
    .secondary-btn > button {
        background: transparent;
        border: 1px solid var(--glass-border);
        color: var(--text-primary);
        box-shadow: none;
    }

    .secondary-btn > button:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: var(--accent-cyan);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
    }

    /* ========================================
       📋 TABS (MOBILE)
       ======================================== */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(10, 10, 15, 0.8);
        border-radius: 16px;
        padding: 0.4rem;
        gap: 0.25rem;
        border: 1px solid var(--glass-border);
        justify-content: center;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: var(--text-muted);
        font-family: var(--font-body);
        font-weight: 500;
        font-size: 0.8rem;
        padding: 0.75rem 1rem;
        border: none;
        flex: 1;
        justify-content: center;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text-secondary);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--accent-green), var(--accent-cyan));
        color: #000;
        font-weight: 600;
    }

    /* ========================================
       📝 INPUT FIELDS (MOBILE)
       ======================================== */
    .stTextInput > div > div > input {
        background: rgba(10, 10, 15, 0.8);
        border: 1px solid var(--glass-border);
        border-radius: 14px;
        color: var(--text-primary);
        font-family: var(--font-body);
        padding: 1rem 1.25rem;
        font-size: 1rem;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--accent-green);
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.15);
    }

    .stTextInput > label {
        font-family: var(--font-body);
        font-size: 0.85rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
    }

    /* ========================================
       📊 METRICS (MOBILE)
       ======================================== */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(15, 15, 20, 0.95), rgba(8, 8, 12, 0.98));
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
    }

    div[data-testid="stMetricLabel"] {
        font-family: var(--font-body);
        font-size: 0.75rem !important;
        color: var(--text-secondary) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    div[data-testid="stMetricValue"] {
        font-family: var(--font-display) !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
    }

    /* ========================================
       👤 PROFILE SECTION
       ======================================== */
    .profile-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .profile-avatar {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--accent-green), var(--accent-cyan));
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        font-family: var(--font-display);
        font-size: 2.5rem;
        font-weight: 700;
        color: #000;
        box-shadow: 0 10px 40px rgba(0, 255, 136, 0.3);
    }

    .profile-name {
        font-family: var(--font-heading);
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }

    .profile-email {
        font-family: var(--font-body);
        font-size: 0.9rem;
        color: var(--text-secondary);
    }

    /* ========================================
       🎬 ANIMATIONS (MOBILE)
       ======================================== */
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    /* Apply animations */
    .score-card { animation: scaleIn 0.5s ease-out; }
    .violation-card { animation: slideUp 0.4s ease-out; }
    .vehicle-card { animation: slideUp 0.4s ease-out; }
    .warning-banner { animation: fadeIn 0.6s ease-out; }

    /* ========================================
       📱 RESPONSIVE
       ======================================== */
    @media (max-width: 480px) {
        .app-title {
            font-size: 1.2rem;
        }

        .score-circle {
            width: 140px;
            height: 140px;
        }

        .score-circle::before {
            width: 110px;
            height: 110px;
        }

        .score-value {
            font-size: 2.5rem;
        }

        .payment-methods {
            grid-template-columns: 1fr;
        }
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

</style>
"""


# ============================================================================
# 🎨 COMPONENT HTML TEMPLATES
# ============================================================================

def get_header_html(title: str = "TRAFFIC CONTROL", subtitle: str = "SYSTEM ONLINE") -> str:
    """Generate header HTML"""
    return f"""
    <div class="main-header">
        <div>
            <div class="header-title">{title}</div>
            <div class="header-subtitle">● {subtitle}</div>
        </div>
        <div class="live-indicator">LIVE</div>
    </div>
    """


def get_stat_card_html(value: str, label: str, delta: str = None, delta_type: str = "positive") -> str:
    """Generate stat card HTML"""
    delta_html = ""
    if delta:
        delta_html = f'<div class="stat-delta {delta_type}">{delta}</div>'
    
    return f"""
    <div class="stat-card">
        <div class="stat-value">{value}</div>
        <div class="stat-label">{label}</div>
        {delta_html}
    </div>
    """


def get_score_card_html(score: int, badge: str = "Good") -> str:
    """Generate score card HTML for mobile app"""
    badge_color = "#00ff88" if badge == "Excellent" else "#00d4ff" if badge == "Good" else "#f59e0b" if badge == "Average" else "#ef4444"
    
    return f"""
    <div class="score-card">
        <div class="score-circle" style="--score: {score};">
            <div class="score-value">{score}</div>
        </div>
        <div class="score-label">Safety Score</div>
        <div class="score-badge" style="border-color: {badge_color}; color: {badge_color};">
            ● {badge}
        </div>
    </div>
    """


def get_violation_card_html(
    violation_type: str,
    location: str,
    date: str,
    fine: float,
    status: str = "pending"
) -> str:
    """Generate violation card HTML"""
    status_class = "paid" if status.lower() == "paid" else "pending"
    card_class = "paid" if status.lower() == "paid" else ""
    
    return f"""
    <div class="violation-card {card_class}">
        <div class="violation-header">
            <div class="violation-type">{violation_type}</div>
            <div class="violation-status {status_class}">{status}</div>
        </div>
        <div class="violation-details">
            <div class="violation-detail">📍 <span>{location}</span></div>
            <div class="violation-detail">📅 <span>{date}</span></div>
        </div>
        <div class="violation-fine">LKR {fine:,.0f}</div>
    </div>
    """


def get_vehicle_card_html(
    plate: str,
    vehicle_type: str,
    color: str = "Unknown",
    make: str = "Unknown"
) -> str:
    """Generate vehicle card HTML"""
    return f"""
    <div class="vehicle-card">
        <div class="vehicle-plate">{plate}</div>
        <div class="vehicle-info">
            <div class="vehicle-info-item">
                <strong>Type</strong>
                {vehicle_type}
            </div>
            <div class="vehicle-info-item">
                <strong>Color</strong>
                {color}
            </div>
            <div class="vehicle-info-item">
                <strong>Make</strong>
                {make}
            </div>
        </div>
    </div>
    """


def get_warning_banner_html(title: str, message: str) -> str:
    """Generate warning banner HTML"""
    return f"""
    <div class="warning-banner">
        <div class="warning-title">{title}</div>
        <div class="warning-message">{message}</div>
    </div>
    """


def get_hero_text_html(lines: list) -> str:
    """Generate hero outline text HTML"""
    html_lines = ""
    for line in lines:
        html_lines += f"<div>{line}</div>"
    
    return f"""
    <div class="hero-text">
        {html_lines}
    </div>
    """


def get_mobile_header_html(title: str = "SAFE DRIVE", subtitle: str = "Driver Assistant") -> str:
    """Generate mobile app header HTML"""
    return f"""
    <div class="app-header">
        <div class="app-logo">SD</div>
        <div class="app-title">{title}</div>
        <div class="app-subtitle">{subtitle}</div>
    </div>
    """


def get_profile_header_html(name: str, email: str, initial: str = None) -> str:
    """Generate profile header HTML"""
    if initial is None:
        initial = name[0].upper() if name else "U"
    
    return f"""
    <div class="profile-header">
        <div class="profile-avatar">{initial}</div>
        <div class="profile-name">{name}</div>
        <div class="profile-email">{email}</div>
    </div>
    """


# ============================================================================
# 🎨 PLOTLY CHART THEME
# ============================================================================
PLOTLY_THEME = {
    "layout": {
        "paper_bgcolor": "rgba(10, 10, 10, 0.8)",
        "plot_bgcolor": "rgba(10, 10, 10, 0.8)",
        "font": {
            "family": "Space Grotesk, sans-serif",
            "color": "#b0b0b0"
        },
        "title": {
            "font": {
                "family": "Orbitron, sans-serif",
                "size": 16,
                "color": "#ffffff"
            }
        },
        "xaxis": {
            "gridcolor": "rgba(255, 255, 255, 0.05)",
            "linecolor": "rgba(255, 255, 255, 0.1)",
            "tickfont": {"color": "#888888"}
        },
        "yaxis": {
            "gridcolor": "rgba(255, 255, 255, 0.05)",
            "linecolor": "rgba(255, 255, 255, 0.1)",
            "tickfont": {"color": "#888888"}
        },
        "colorway": ["#00ff88", "#00d4ff", "#8b5cf6", "#f59e0b", "#ef4444"],
        "margin": {"t": 50, "b": 50, "l": 50, "r": 30}
    }
}


def apply_plotly_theme(fig):
    """Apply dark theme to Plotly figure"""
    fig.update_layout(
        paper_bgcolor="rgba(10, 10, 10, 0.8)",
        plot_bgcolor="rgba(10, 10, 10, 0.8)",
        font=dict(family="Space Grotesk, sans-serif", color="#b0b0b0"),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.05)",
            linecolor="rgba(255, 255, 255, 0.1)",
            tickfont=dict(color="#888888")
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.05)",
            linecolor="rgba(255, 255, 255, 0.1)",
            tickfont=dict(color="#888888")
        ),
        margin=dict(t=50, b=50, l=50, r=30)
    )
    return fig


# ============================================================================
# 📊 COLOR SEQUENCES FOR CHARTS
# ============================================================================
CHART_COLORS = [
    "#00ff88",  # Green
    "#00d4ff",  # Cyan
    "#8b5cf6",  # Purple
    "#f59e0b",  # Amber
    "#ef4444",  # Red
    "#ec4899",  # Pink
    "#14b8a6",  # Teal
]

SEVERITY_COLORS = {
    "low": "#00ff88",
    "medium": "#f59e0b",
    "high": "#ef4444",
    "severe": "#dc2626"
}

STATUS_COLORS = {
    "pending": "#f59e0b",
    "paid": "#00ff88",
    "unpaid": "#ef4444",
    "reviewed": "#00d4ff",
    "warning": "#f59e0b"
}