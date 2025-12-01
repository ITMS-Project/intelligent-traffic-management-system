
"""
Custom CSS styles for the Intelligent Traffic Management System
"""

# Dashboard Styles (AR/HUD Look)
DASHBOARD_CSS = """
<style>
    /* Global Settings */
    .stApp {
        background-color: #050505;
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header */
    .main-header {
        background: rgba(20, 20, 20, 0.6);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1rem;
        position: sticky;
        top: 0;
        z-index: 999;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .header-title {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #fff, #aaa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
    }
    
    /* Sidebar (Glassmorphism) */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 10, 10, 0.8);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Buttons (Orange Accent) */
    .stButton > button {
        background: linear-gradient(90deg, #FF7F50, #FF4500);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(255, 69, 0, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 69, 0, 0.5);
    }
    
    /* Metrics (HUD Panels) */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        backdrop-filter: blur(5px);
    }
    
    div[data-testid="stMetricLabel"] {
        color: #888;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div[data-testid="stMetricValue"] {
        color: #fff;
        font-size: 1.8rem;
        font-weight: 300;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }
    
    /* Video Container */
    .video-container {
        border: 1px solid rgba(255, 127, 80, 0.3);
        border-radius: 4px;
        position: relative;
        overflow: hidden;
    }
    
    .video-container::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        border: 1px solid rgba(255, 127, 80, 0.1);
        pointer-events: none;
        z-index: 10;
        background: 
            linear-gradient(to right, rgba(255,127,80,0.5) 1px, transparent 1px) 0 0,
            linear-gradient(to bottom, rgba(255,127,80,0.5) 1px, transparent 1px) 0 0;
        background-size: 20px 20px;
        opacity: 0.05;
    }
    
    /* Custom HUD Elements */
    .hud-corner {
        position: absolute;
        width: 20px;
        height: 20px;
        border: 2px solid #FF7F50;
        z-index: 20;
    }
    .top-left { top: 10px; left: 10px; border-right: 0; border-bottom: 0; }
    .top-right { top: 10px; right: 10px; border-left: 0; border-bottom: 0; }
    .bottom-left { bottom: 10px; left: 10px; border-right: 0; border-top: 0; }
    .bottom-right { bottom: 10px; right: 10px; border-left: 0; border-top: 0; }

</style>
"""

# Mobile App Styles (Modern Automotive Look)
MOBILE_CSS = """
<style>
    /* Global Settings */
    .stApp {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header */
    .app-header {
        background: transparent;
        padding: 2rem 1rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .app-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(46, 134, 222, 0.2) 0%, transparent 70%);
        z-index: -1;
    }
    
    .app-title {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
        background: linear-gradient(180deg, #fff, #ccc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .app-subtitle {
        font-size: 0.9rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Cards (Glassmorphism) */
    .violation-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    
    .violation-card:active {
        transform: scale(0.98);
    }
    
    /* Status Badges */
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .status-pending { background: rgba(255, 71, 87, 0.2); color: #ff4757; border: 1px solid rgba(255, 71, 87, 0.3); }
    .status-paid { background: rgba(46, 213, 115, 0.2); color: #2ed573; border: 1px solid rgba(46, 213, 115, 0.3); }
    
    /* Buttons (Blue Pill) */
    .stButton > button {
        background: #2E86DE;
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1rem;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 4px 15px rgba(46, 134, 222, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #54a0ff;
        box-shadow: 0 6px 20px rgba(46, 134, 222, 0.6);
        transform: translateY(-2px);
    }
    
    /* Inputs */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2E86DE;
        box-shadow: 0 0 0 2px rgba(46, 134, 222, 0.2);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: nowrap;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        color: #888;
        border: none;
        padding: 0 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2E86DE;
        color: white;
    }
    
</style>
"""
