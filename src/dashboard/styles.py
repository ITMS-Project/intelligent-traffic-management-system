"""
🎨 CYBERPUNK NEON UI STYLES
Intelligent Traffic Management System
Colors: Neon Green (#00ff88), Cyan (#00d4ff), Pure Black (#000000)
"""
from pathlib import Path
import base64

def get_base64_image(image_path):
    """Get base64 encoding of image"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

# Load background image
bg_image_path = Path(__file__).parent / "assets" / "background.png"
bg_base64 = get_base64_image(bg_image_path)

# ============================================================================
# 🎨 COLOR PALETTE - CYBERPUNK NEON
# ============================================================================
# ============================================================================
# 🎨 COLOR PALETTE - PREMIUM MONOCHROME
# ============================================================================
COLORS = {
    # Primary Dark Theme
    "bg_primary": "#000000",
    "bg_secondary": "#0a0a0a",
    "bg_tertiary": "#111111",
    "bg_card": "rgba(20, 20, 20, 0.9)",
    
    # Monochrome Accents
    "accent_primary": "#ffffff",      # White
    "accent_secondary": "#888888",    # Gray
    "accent_warning": "#ffffff",      # White (for warnings, maybe bold)
    "accent_danger": "#ffffff",       # White
    "accent_success": "#ffffff",      # White
    
    # Text Colors
    "white": "#ffffff",
    "gray_light": "#cccccc",
    "gray_medium": "#888888",
    "gray_dark": "#444444",
    
    # Glass Effects
    "glass_bg": "rgba(255, 255, 255, 0.05)",
    "glass_border": "rgba(255, 255, 255, 0.1)",
}

# ============================================================================
# 🎬 AUTHORITY DASHBOARD STYLES (Cyberpunk Neon)
# ============================================================================
DASHBOARD_CSS = """
<style>
    /* ========================================
       🌐 GOOGLE FONTS IMPORT
       ======================================== */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    /* ========================================
       🎨 CSS VARIABLES - MONOCHROME
       ======================================== */
    :root {
        --bg-primary: #000000;
        --bg-secondary: #0a0a0a;
        --bg-tertiary: #111111;
        --bg-card: rgba(20, 20, 20, 0.95);
        
        --accent-primary: #ffffff;
        --accent-secondary: #888888;
        
        --white: #ffffff;
        --gray-100: #e0e0e0;
        --gray-200: #cccccc;
        --gray-300: #888888;
        --gray-400: #666666;
        --gray-500: #444444;
        
        --text-primary: #ffffff;
        --text-secondary: #aaaaaa;
        --text-muted: #666666;
        
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.15);
        
        --font-display: 'Orbitron', sans-serif;
        --font-heading: 'Rajdhani', sans-serif;
        --font-body: 'Inter', 'Space Grotesk', sans-serif;
        
        --transition-fast: 0.15s ease;
        --transition-normal: 0.3s ease;
    }

    /* ========================================
       🌌 BACKGROUND - MONOCHROME
       ======================================== */
    .stApp {
        background: #000000;
        min-height: 100vh;
        font-family: var(--font-body);
        color: var(--text-primary);
        position: relative;
        overflow-x: hidden;
    }

    /* Background Image Overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at center, rgba(30, 30, 30, 0.5) 0%, #000000 100%);
        pointer-events: none;
        z-index: 0;
    }

    /* Ensure content is above background */
    .main .block-container {
        position: relative;
        z-index: 1;
    }

    section[data-testid="stSidebar"] {
        z-index: 2;
    }

    /* ========================================
       🎯 MAIN HEADER - MONOCHROME
       ======================================== */
    .main-header {
        background: linear-gradient(135deg, rgba(20, 20, 20, 0.9), rgba(10, 10, 10, 0.95));
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 2px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--white);
    }

    .header-title {
        font-family: var(--font-display);
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: 4px;
        color: var(--white);
        text-transform: uppercase;
    }

    .header-subtitle {
        font-family: var(--font-body);
        font-size: 0.75rem;
        color: var(--gray-300);
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 0.25rem;
    }

    /* ========================================
       🎴 GLASSMORPHISM CARDS - MONOCHROME
       ======================================== */
    .glass-card {
        background: rgba(20, 20, 20, 0.8);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: 4px;
        padding: 1.5rem;
        position: relative;
        transition: all var(--transition-normal);
    }    animation: fadeInUp 0.5s ease-out;
    }

    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--neon-green), transparent);
    }

    .glass-card:hover {
        border-color: rgba(0, 255, 136, 0.4);
        transform: translateY(-4px);
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.4),
            0 0 30px rgba(0, 255, 136, 0.1);
    }

    /* ========================================
       📊 STREAMLIT METRIC OVERRIDE - MONOCHROME
       ======================================== */
    div[data-testid="stMetric"] {
        background: rgba(20, 20, 20, 0.8);
        border: 1px solid var(--glass-border);
        border-radius: 4px;
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
        width: 4px;
        height: 100%;
        background: var(--white);
    }

    div[data-testid="stMetric"]:hover {
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
    }

    div[data-testid="stMetricLabel"] {
        font-family: var(--font-body);
        font-size: 0.75rem !important;
        color: var(--gray-300) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    div[data-testid="stMetricValue"] {
        font-family: var(--font-display) !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: var(--white) !important;
    }

    div[data-testid="stMetricDelta"] {
        font-family: var(--font-body);
        font-size: 0.85rem !important;
        color: var(--gray-200) !important;
    }

    /* ========================================
       🔘 BUTTONS - MONOCHROME
       ======================================== */
    .stButton > button {
        background: var(--white);
        color: #000000;
        border: none;
        border-radius: 2px;
        padding: 0.75rem 2rem;
        font-family: var(--font-body);
        font-weight: 600;
        font-size: 0.9rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: all var(--transition-normal);
    }

    .stButton > button:hover {
        background: #e0e0e0;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    /* ========================================
       📝 INPUT FIELDS - MONOCHROME
       ======================================== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--glass-border);
        border-radius: 2px;
        color: var(--white);
        font-family: var(--font-body);
        padding: 0.75rem 1rem;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--white);
        box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.2);
    }

    .stTextInput > label,
    .stNumberInput > label,
    .stTextArea > label,
    .stSelectbox > label {
        font-family: var(--font-body);
        font-size: 0.8rem;
        color: var(--gray-300);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ========================================
       📋 SELECT BOXES - MONOCHROME
       ======================================== */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--glass-border);
        border-radius: 2px;
    }

    .stSelectbox > div > div:hover {
        border-color: rgba(255, 255, 255, 0.3);
    }

    /* ========================================
       🗂️ TABS - MONOCHROME
       ======================================== */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        border-bottom: 1px solid var(--glass-border);
        padding: 0;
        gap: 2rem;
        border-radius: 0;
        border: none;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 0;
        color: var(--gray-400);
        font-family: var(--font-body);
        font-weight: 500;
        font-size: 0.9rem;
        padding: 0.75rem 0;
        border: none;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--white);
        background: transparent;
    }

    .stTabs [aria-selected="true"] {
        background: transparent;
        color: var(--white);
        font-weight: 600;
        border-bottom: 2px solid var(--white);
        box-shadow: none;
    }

    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* ========================================
       📊 DATAFRAMES & TABLES - NEON
       ======================================== */
    .stDataFrame {
        background: rgba(0, 0, 0, 0.7);
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(0, 255, 136, 0.15);
    }

    .stDataFrame thead tr th {
        background: rgba(0, 255, 136, 0.1);
        color: var(--neon-green);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.75rem;
    }

    .stDataFrame tbody tr {
        transition: background var(--transition-fast);
    }

    .stDataFrame tbody tr:hover {
        background: rgba(0, 255, 136, 0.05);
    }

    /* Sidebar is globally hidden at the end of file */

    /* Background Image Overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url("data:image/png;base64,__BG_IMAGE_PLACEHOLDER__");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0.4;
        z-index: 0;
        pointer-events: none;
    }

    /* ========================================
       📝 FILE UPLOADER - NEON
       ======================================== */
    .stFileUploader {
        background: rgba(0, 0, 0, 0.5);
        border: 2px dashed rgba(0, 255, 136, 0.3);
        border-radius: 16px;
        transition: all var(--transition-normal);
    }

    .stFileUploader:hover {
        border-color: var(--neon-green);
        background: rgba(0, 255, 136, 0.05);
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.1);
    }

    /* ========================================
       ⏳ PROGRESS BAR - NEON
       ======================================== */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--neon-green), var(--neon-cyan));
        border-radius: 10px;
        height: 8px;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
    }

    .stProgress > div > div {
        background: rgba(0, 255, 136, 0.1);
        border-radius: 10px;
    }

    /* ========================================
       🎯 STATUS BADGES - MONOCHROME
       ======================================== */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 1rem;
        border-radius: 4px;
        font-family: var(--font-body);
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .status-badge.online {
        background: rgba(255, 255, 255, 0.1);
        color: var(--white);
        border: 1px solid var(--glass-border);
    }

    .status-badge.online::before {
        content: '';
        width: 6px;
        height: 6px;
        background: var(--white);
        border-radius: 50%;
        box-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
        animation: statusPulse 2s ease-in-out infinite;
    }

    @keyframes statusPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
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

    @keyframes neonFlicker {
        0%, 100% { opacity: 1; }
        92% { opacity: 1; }
        93% { opacity: 0.8; }
        94% { opacity: 1; }
        96% { opacity: 0.9; }
        97% { opacity: 1; }
    }

    @keyframes scanLine {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(100vh); }
    }

    /* Staggered Animations */
    .animate-1 { animation-delay: 0.1s; }
    .animate-2 { animation-delay: 0.2s; }
    .animate-3 { animation-delay: 0.3s; }
    .animate-4 { animation-delay: 0.4s; }

    /* ========================================
       🎨 HERO TEXT - MONOCHROME
       ======================================== */
    .hero-text {
        font-family: var(--font-display);
        font-size: 4.5rem;
        font-weight: 900;
        color: var(--white);
        text-transform: uppercase;
        letter-spacing: 4px;
        line-height: 1.1;
        text-align: center;
        margin-bottom: 3rem;
    }

    .hero-text span {
        color: var(--gray-300);
    }

    /* ========================================
       🔴 LIVE INDICATOR - MONOCHROME
       ======================================== */
    .live-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1.25rem;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid var(--glass-border);
        border-radius: 4px;
        font-family: var(--font-body);
        font-size: 0.75rem;
        color: var(--white);
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .live-indicator::before {
        content: '';
        width: 8px;
        height: 8px;
        background: #ff0000;
        border-radius: 50%;
        box-shadow: 0 0 10px #ff0000;
        animation: livePulse 2s ease-in-out infinite;
    }

    @keyframes livePulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    /* ========================================
       📊 STAT CARD - MONOCHROME
       ======================================== */
    .stat-card-floating {
        background: rgba(20, 20, 20, 0.8);
        border: 1px solid var(--glass-border);
        border-radius: 4px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .stat-card-floating:hover {
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
    }

    .stat-card-floating::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--white);
    }

    .stat-value-large {
        font-family: var(--font-display);
        font-size: 3rem;
        font-weight: 700;
        color: var(--white);
        line-height: 1;
    }

    .stat-label-small {
        font-family: var(--font-body);
        font-size: 0.8rem;
        color: var(--gray-300);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }

    /* ========================================
       📱 RESPONSIVE
       ======================================== */
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem;
            flex-direction: column;
            gap: 1rem;
        }

        .header-title {
            font-size: 1.2rem;
            letter-spacing: 3px;
        }

        .hero-text {
            font-size: 2.5rem;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
    }

    /* ========================================
       🔧 UTILITY CLASSES
       ======================================== */
    .text-neon-green { color: var(--neon-green); text-shadow: 0 0 10px rgba(0, 255, 136, 0.5); }
    .text-neon-cyan { color: var(--neon-cyan); text-shadow: 0 0 10px rgba(0, 212, 255, 0.5); }
    .text-white { color: var(--white); }
    .text-gray { color: var(--gray-300); }
    
    .glow-green { box-shadow: 0 0 30px rgba(0, 255, 136, 0.3); }
    .glow-cyan { box-shadow: 0 0 30px rgba(0, 212, 255, 0.3); }
    
    .border-neon {
        border: 1px solid rgba(0, 255, 136, 0.3);
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

</style>

<!-- Floating Particles HTML (Removed for Monochrome) -->
<!-- <div class="particles">...</div> -->
"""


# ============================================================================
# 📱 MOBILE DRIVER APP STYLES (Cyberpunk Neon)
# ============================================================================
MOBILE_CSS = """
<style>
    /* ========================================
       🌐 GOOGLE FONTS IMPORT
       ======================================== */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    /* ========================================
       🎨 CSS VARIABLES - MONOCHROME
       ======================================== */
    :root {
        --bg-primary: #000000;
        --bg-secondary: #0a0a0a;
        --bg-card: rgba(20, 20, 20, 0.9);
        
        --white: #ffffff;
        --gray-300: #888888;
        --gray-400: #666666;
        --gray-500: #444444;
        
        --font-display: 'Orbitron', sans-serif;
        --font-heading: 'Rajdhani', sans-serif;
        --font-body: 'Inter', sans-serif;
    }

    /* ========================================
       🌌 BACKGROUND - MONOCHROME
       ======================================== */
    .stApp {
        background: #000000;
        min-height: 100vh;
        font-family: var(--font-body);
        color: var(--white);
        position: relative;
    }

    /* Background Image Overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at center, rgba(30, 30, 30, 0.5) 0%, #000000 100%);
        pointer-events: none;
        z-index: 0;
    }

    .stApp::after {
        display: none;
    }

    .main .block-container {
        position: relative;
        z-index: 1;
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
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, var(--neon-green), var(--neon-cyan));
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        font-family: var(--font-display);
        font-size: 1.8rem;
        font-weight: 700;
        color: #000;
        box-shadow: 
            0 10px 40px rgba(0, 255, 136, 0.3),
            0 0 60px rgba(0, 255, 136, 0.2);
    }

    .app-title {
        font-family: var(--font-display);
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: 4px;
        color: var(--white);
        margin-bottom: 0.25rem;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
    }

    .app-subtitle {
        font-family: var(--font-body);
        font-size: 0.8rem;
        color: var(--neon-green);
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* ========================================
       🏆 SAFETY SCORE CARD - NEON
       ======================================== */
    .score-card {
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.85), rgba(10, 10, 10, 0.9));
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 24px;
        padding: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 40px rgba(0, 255, 136, 0.1);
    }

    .score-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--neon-green), var(--neon-cyan), transparent);
    }

    .score-circle {
        width: 180px;
        height: 180px;
        border-radius: 50%;
        background: conic-gradient(
            var(--neon-green) calc(var(--score) * 3.6deg),
            rgba(0, 255, 136, 0.1) 0deg
        );
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        position: relative;
        box-shadow: 
            0 0 50px rgba(0, 255, 136, 0.3),
            inset 0 0 30px rgba(0, 0, 0, 0.5);
    }

    .score-circle::before {
        content: '';
        position: absolute;
        width: 150px;
        height: 150px;
        background: linear-gradient(145deg, #0a0a0a, #050505);
        border-radius: 50%;
    }

    .score-value {
        position: relative;
        z-index: 1;
        font-family: var(--font-display);
        font-size: 3.5rem;
        font-weight: 700;
        color: var(--neon-green);
        text-shadow: 0 0 30px rgba(0, 255, 136, 0.5);
    }

    .score-label {
        font-family: var(--font-body);
        font-size: 0.9rem;
        color: var(--gray-300);
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .score-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1.5rem;
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 50px;
        font-family: var(--font-body);
        font-size: 0.85rem;
        color: var(--neon-green);
        margin-top: 1rem;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
    }

    /* ========================================
       📋 VIOLATION CARD - NEON
       ======================================== */
    .violation-card {
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.85), rgba(10, 10, 10, 0.9));
        border: 1px solid rgba(0, 255, 136, 0.15);
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
        background: linear-gradient(180deg, var(--neon-green), var(--neon-cyan));
        border-radius: 4px 0 0 4px;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.5);
    }

    .violation-card:hover {
        transform: translateX(8px);
        border-color: rgba(0, 255, 136, 0.3);
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.1);
    }

    .violation-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 0.75rem;
    }

    .violation-type {
        font-family: var(--font-heading);
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--white);
    }

    .violation-status {
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-family: var(--font-body);
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .violation-status.pending {
        background: rgba(255, 170, 0, 0.15);
        color: #ffaa00;
        border: 1px solid rgba(255, 170, 0, 0.3);
    }

    .violation-status.paid {
        background: rgba(0, 255, 136, 0.15);
        color: var(--neon-green);
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
        color: var(--gray-400);
    }

    .violation-detail span {
        color: var(--gray-300);
        font-weight: 500;
    }

    .violation-fine {
        font-family: var(--font-display);
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--neon-cyan);
        text-align: right;
        text-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
    }

    /* ========================================
       🚗 VEHICLE CARD - NEON
       ======================================== */
    .vehicle-card {
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.85), rgba(10, 10, 10, 0.9));
        border: 1px solid rgba(0, 255, 136, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }

    .vehicle-card:hover {
        border-color: rgba(0, 255, 136, 0.4);
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(0, 255, 136, 0.15);
    }

    .vehicle-plate {
        font-family: var(--font-display);
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--neon-green);
        padding: 0.5rem 1.25rem;
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 10px;
        display: inline-block;
        margin-bottom: 1rem;
        letter-spacing: 3px;
        text-shadow: 0 0 15px rgba(0, 255, 136, 0.5);
    }

    .vehicle-info {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
    }

    .vehicle-info-item {
        font-family: var(--font-body);
        font-size: 0.85rem;
        color: var(--gray-400);
    }

    .vehicle-info-item strong {
        color: var(--neon-cyan);
        display: block;
        margin-bottom: 0.25rem;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ========================================
       ⚠️ WARNING BANNER - NEON
       ======================================== */
    .warning-banner {
        background: linear-gradient(135deg, rgba(255, 170, 0, 0.15), rgba(255, 100, 0, 0.1));
        border: 1px solid rgba(255, 170, 0, 0.3);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        animation: warningPulse 2s ease-in-out infinite;
    }

    @keyframes warningPulse {
        0%, 100% { box-shadow: 0 0 20px rgba(255, 170, 0, 0.2); }
        50% { box-shadow: 0 0 40px rgba(255, 170, 0, 0.4); }
    }

    .warning-banner::before {
        content: '⚠️';
        position: absolute;
        top: 50%;
        right: 1rem;
        transform: translateY(-50%);
        font-size: 2.5rem;
        opacity: 0.3;
    }

    .warning-title {
        font-family: var(--font-heading);
        font-size: 1.1rem;
        font-weight: 700;
        color: #ffaa00;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-shadow: 0 0 15px rgba(255, 170, 0, 0.5);
    }

    .warning-message {
        font-family: var(--font-body);
        font-size: 0.9rem;
        color: var(--gray-300);
        line-height: 1.5;
    }

    /* ========================================
       🔘 BUTTONS (MOBILE) - NEON
       ======================================== */
    /* ========================================
       🔘 BUTTONS (MOBILE) - MONOCHROME FIX
       ======================================== */
    div.stButton > button {
        background: linear-gradient(145deg, #1a1a1a, #0a0a0a) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
        width: 100% !important;
    }

    div.stButton > button:hover {
        background: #ffffff !important;
        color: #000000 !important;
        border-color: #ffffff !important;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.4) !important;
        transform: translateY(-2px) !important;
    }

    div.stButton > button:active {
        transform: translateY(1px) !important;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.2) !important;
    }

    /* ========================================
       📋 TABS (MOBILE) - NEON
       ======================================== */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(0, 0, 0, 0.7);
        border-radius: 16px;
        padding: 0.4rem;
        gap: 0.25rem;
        border: 1px solid rgba(0, 255, 136, 0.1);
        justify-content: center;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: var(--gray-400);
        font-family: var(--font-body);
        font-weight: 500;
        font-size: 0.8rem;
        padding: 0.75rem 1rem;
        border: none;
        flex: 1;
        justify-content: center;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--neon-green);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--neon-green), var(--neon-cyan));
        color: #000000;
        font-weight: 700;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
    }

    /* ========================================
       📝 INPUT FIELDS (MOBILE) - NEON
       ======================================== */
    .stTextInput > div > div > input {
        background: rgba(0, 0, 0, 0.7);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 14px;
        color: var(--white);
        font-family: var(--font-body);
        padding: 1rem 1.25rem;
        font-size: 1rem;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--neon-green);
        box-shadow: 0 0 25px rgba(0, 255, 136, 0.3);
    }

    /* ========================================
       📊 METRICS (MOBILE) - NEON
       ======================================== */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.85), rgba(10, 10, 10, 0.9));
        border: 1px solid rgba(0, 255, 136, 0.15);
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
    }

    div[data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--neon-green), var(--neon-cyan));
    }

    div[data-testid="stMetricLabel"] {
        font-family: var(--font-body);
        font-size: 0.7rem !important;
        color: var(--gray-400) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    div[data-testid="stMetricValue"] {
        font-family: var(--font-display) !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: var(--neon-green) !important;
        text-shadow: 0 0 15px rgba(0, 255, 136, 0.5);
    }

    /* ========================================
       👤 PROFILE SECTION - NEON
       ======================================== */
    .profile-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .profile-avatar {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--neon-green), var(--neon-cyan));
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        font-family: var(--font-display);
        font-size: 2.5rem;
        font-weight: 700;
        color: #000;
        box-shadow: 
            0 10px 50px rgba(0, 255, 136, 0.3),
            0 0 80px rgba(0, 255, 136, 0.2);
    }

    .profile-name {
        font-family: var(--font-heading);
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--white);
        margin-bottom: 0.25rem;
    }

    .profile-email {
        font-family: var(--font-body);
        font-size: 0.9rem;
        color: var(--neon-cyan);
    }

    /* ========================================
       🎬 ANIMATIONS
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

    .score-card { animation: scaleIn 0.5s ease-out; }
    .violation-card { animation: slideUp 0.4s ease-out; }
    .vehicle-card { animation: slideUp 0.4s ease-out; }

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

    /* ========================================
       📱 RESPONSIVE
       ======================================== */
    @media (max-width: 480px) {
        .app-title { font-size: 1.3rem; }
        .score-circle { width: 150px; height: 150px; }
        .score-circle::before { width: 120px; height: 120px; }
        .score-value { font-size: 2.8rem; }
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* header {visibility: hidden;} */

    /* PERMANENTLY HIDE SIDEBAR & TOGGLE */
    section[data-testid="stSidebar"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"],
    button[kind="header"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
    
    /* Ensure Header is Visible and Clickable */
    header[data-testid="stHeader"] {
        background: transparent !important;
        z-index: 10 !important;
        visibility: visible !important;
        height: auto !important;
        pointer-events: none !important;
    }

    /* Custom Progress Bar Color - High Specificity */
    .stProgress > div > div > div > div {
        background-color: #cccccc !important;
    }
    div[data-testid="stProgress"] > div > div > div > div {
        background-color: #cccccc !important;
    }
    /* Target inner bar specifically */
    .stProgress .st-bo {
        background-color: #cccccc !important;
    }
    /* Fallback for other potential class names */
    div[role="progressbar"] > div {
        background-color: #cccccc !important;
    }

</style>
"""

# Inject background image
DASHBOARD_CSS = DASHBOARD_CSS.replace("__BG_IMAGE_PLACEHOLDER__", bg_base64)


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


def get_stat_card_html(value: str, label: str, delta: str = None) -> str:
    """Generate floating stat card HTML"""
    delta_html = f'<div style="font-size: 0.8rem; color: #cccccc; margin-top: 0.5rem;">{delta}</div>' if delta else ""
    
    return f"""
    <div class="stat-card-floating">
        <div class="stat-value-large">{value}</div>
        <div class="stat-label-small">{label}</div>
        {delta_html}
    </div>
    """


def get_score_card_html(score: int, badge: str = "Good") -> str:
    """Generate score card HTML for mobile app"""
    return f"""
    <div class="score-card">
        <div class="score-circle" style="--score: {score};">
            <div class="score-value">{score}</div>
        </div>
        <div class="score-label">Safety Score</div>
        <div class="score-badge">★ {badge}</div>
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
    
    return f"""
    <div class="violation-card">
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
    for i, line in enumerate(lines):
        if i == 1:
            html_lines += f"<div><span>{line}</span></div>"
        else:
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
        <div class="app-logo" style="background: #ffffff; color: #000000; box-shadow: 0 10px 30px rgba(255,255,255,0.2);">SD</div>
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
        <div class="profile-avatar" style="background: #ffffff; color: #000000; box-shadow: 0 10px 30px rgba(255,255,255,0.2);">{initial}</div>
        <div class="profile-name">{name}</div>
        <div class="profile-email" style="color: #888888;">{email}</div>
    </div>
    """


# ============================================================================
# 🎨 PLOTLY CHART THEME - MONOCHROME
# ============================================================================
def apply_plotly_theme(fig):
    """Apply monochrome dark theme to Plotly figure"""
    fig.update_layout(
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(family="Inter, sans-serif", color="#cccccc"),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.1)",
            linecolor="rgba(255, 255, 255, 0.2)",
            tickfont=dict(color="#888888")
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.1)",
            linecolor="rgba(255, 255, 255, 0.2)",
            tickfont=dict(color="#888888")
        ),
        margin=dict(t=50, b=50, l=50, r=30)
    )
    return fig


# ============================================================================
# 📊 COLOR SEQUENCES FOR CHARTS - MONOCHROME
# ============================================================================
CHART_COLORS = [
    "#ffffff",  # White
    "#cccccc",  # Light Gray
    "#888888",  # Medium Gray
    "#444444",  # Dark Gray
    "#aaaaaa",  # Silver
]

SEVERITY_COLORS = {
    "low": "#888888",
    "medium": "#cccccc",
    "high": "#ffffff",
    "severe": "#ffffff"  # Maybe add a border or pattern for severe
}

STATUS_COLORS = {
    "pending": "#cccccc",
    "paid": "#ffffff",
    "unpaid": "#888888",
    "reviewed": "#aaaaaa",
    "warning": "#ffffff"
}