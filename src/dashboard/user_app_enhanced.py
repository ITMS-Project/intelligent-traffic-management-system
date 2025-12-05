"""
📱 DRIVER MOBILE APP - Premium Monochrome Design
Intelligent Traffic Management System
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random
import plotly.graph_objects as go
import pandas as pd

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.dashboard.styles import (
    MOBILE_CSS,
    get_score_card_html,
    get_violation_card_html,
    get_vehicle_card_html,
    get_warning_banner_html,
    get_mobile_header_html,
    get_profile_header_html,
    get_profile_header_html,
    apply_plotly_theme
)
import base64
from gtts import gTTS
import io

def play_voice_warning(text):
    """Generate and play voice warning using gTTS"""
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        b64 = base64.b64encode(fp.read()).decode()
        
        # Auto-play audio using HTML5 audio tag
        md = f"""
            <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Audio Error: {e}")

# ============================================================================
# 🎯 PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="SafeDrive - Driver App",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply Premium Mobile CSS
# Apply Premium Mobile CSS
st.markdown(MOBILE_CSS, unsafe_allow_html=True)


# ============================================================================
# 🔐 AUTHENTICATION
# ============================================================================
def show_login():
    """Show login/register screen - Monochrome"""
    
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem 2rem;">
        <div style="
            width: 80px;
            height: 80px;
            background: #ffffff;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1.5rem;
            font-family: 'Orbitron', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            color: #000000;
            box-shadow: 0 15px 50px rgba(255, 255, 255, 0.15);
        ">SD</div>
        <div style="font-family: 'Orbitron', sans-serif; font-size: 1.8rem; color: #ffffff; letter-spacing: 4px; margin-bottom: 0.5rem;">
            SAFEDRIVE
        </div>
        <div style="color: #666; font-size: 0.85rem; letter-spacing: 2px; text-transform: uppercase;">
            Driver Assistant
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
    
    with tab1:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        phone = st.text_input("Phone Number", placeholder="Enter your phone number", key="login_phone")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="login_pass")
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        if st.button("LOGIN", type="primary", use_container_width=True):
            if phone and password:
                st.session_state.logged_in = True
                st.session_state.user = {
                    "name": "John Driver",
                    "phone": phone,
                    "email": "john@example.com",
                    "score": 85,
                    "member_since": "Jan 2024"
                }
                st.rerun()
            else:
                st.error("Please enter phone and password")
        
        st.markdown("""
        <div style="text-align: center; margin-top: 1.5rem;">
            <a href="#" style="color: #888; text-decoration: none; font-size: 0.85rem;">Forgot Password?</a>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        reg_name = st.text_input("Full Name", placeholder="Enter your full name", key="reg_name")
        reg_phone = st.text_input("Phone Number", placeholder="Enter phone number", key="reg_phone")
        reg_email = st.text_input("Email", placeholder="Enter email address", key="reg_email")
        reg_vehicle = st.text_input("Vehicle Plate", placeholder="e.g., CAB-1234", key="reg_vehicle")
        reg_type = st.selectbox("Vehicle Type", ["Car", "TukTuk", "Van", "Motorcycle", "Bus", "Truck"])
        reg_password = st.text_input("Password", type="password", placeholder="Create password", key="reg_pass")
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        if st.button("CREATE ACCOUNT", type="primary", use_container_width=True):
            if reg_name and reg_phone and reg_password:
                st.session_state.logged_in = True
                st.session_state.user = {
                    "name": reg_name,
                    "phone": reg_phone,
                    "email": reg_email,
                    "score": 100,
                    "member_since": datetime.now().strftime("%b %Y")
                }
                st.rerun()
            else:
                st.error("Please fill in all required fields")


# ============================================================================
# 🏠 HOME TAB
# ============================================================================
def show_home_tab():
    """Show home screen with safety score - Monochrome"""
    
    user = st.session_state.user
    score = user.get("score", 85)
    
    # Active warning banner
    if random.random() > 0.5:
        st.markdown(get_warning_banner_html(
            "⚠️ APPROACHING NO-PARKING ZONE",
            "You are 200m from Pettah Market restricted area. Please find authorized parking."
        ), unsafe_allow_html=True)
        
        # Play voice warning if not already played for this session
        if 'warning_played' not in st.session_state:
            play_voice_warning("Warning. You are approaching a no parking zone. Please find authorized parking.")
            st.session_state.warning_played = True
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ I'VE MOVED", use_container_width=True):
                st.success("Thank you! Warning dismissed.")
        with col2:
            if st.button("🅿️ FIND PARKING", use_container_width=True):
                st.info("Opening nearby parking locations...")
    
    # Safety Score Card
    badge = "Excellent" if score >= 90 else "Good" if score >= 70 else "Average" if score >= 50 else "Poor"
    st.markdown(get_score_card_html(score, badge), unsafe_allow_html=True)
    
    # Quick Stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Violations", "3", "-1 this month")
    with col2:
        st.metric("Pending Fines", "LKR 5,500")
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Score History Chart
    st.markdown("""
    <div style="
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        color: #ffffff;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    ">30-Day Score History</div>
    """, unsafe_allow_html=True)
    
    days = list(range(30))
    scores = [85 + random.randint(-5, 5) for _ in range(30)]
    scores[-1] = score
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=days,
        y=scores,
        mode='lines',
        fill='tozeroy',
        line=dict(color='#ffffff', width=2),
        fillcolor='rgba(255, 255, 255, 0.1)',
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(10, 10, 10, 0.8)',
        plot_bgcolor='rgba(10, 10, 10, 0.8)',
        margin=dict(t=10, b=30, l=40, r=10),
        height=180,
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.03)',
            tickfont=dict(color='#666', size=10),
            range=[50, 100]
        ),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Recent Activity
    st.markdown("""
    <div style="
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        color: #ffffff;
        margin: 1.5rem 0 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    ">Recent Activity</div>
    """, unsafe_allow_html=True)
    
    activities = [
        {"icon": "⚠️", "text": "Warning received - Pettah area", "time": "2 hours ago", "color": "#888"},
        {"icon": "🎯", "text": "Score increased +5 points", "time": "Yesterday", "color": "#ffffff"},
        {"icon": "💳", "text": "Fine paid - LKR 2,000", "time": "2 days ago", "color": "#c0c0c0"},
    ]
    
    for activity in activities:
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 0.75rem;
            background: rgba(15, 15, 15, 0.6);
            border-radius: 12px;
            margin-bottom: 0.5rem;
        ">
            <span style="font-size: 1.25rem;">{activity['icon']}</span>
            <div style="flex: 1;">
                <div style="color: #e0e0e0; font-size: 0.9rem;">{activity['text']}</div>
                <div style="color: #666; font-size: 0.75rem;">{activity['time']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# 📋 VIOLATIONS TAB
# ============================================================================
def show_violations_tab():
    """Show violations list - Monochrome"""
    
    st.markdown("""
    <div style="
        font-family: 'Orbitron', sans-serif;
        font-size: 1.25rem;
        color: #ffffff;
        margin-bottom: 1.5rem;
        letter-spacing: 2px;
    ">MY VIOLATIONS</div>
    """, unsafe_allow_html=True)
    
    status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Paid"], key="vio_filter")
    
    violations = [
        {"type": "Illegal Parking", "location": "Pettah Market", "date": "Dec 3, 2024", "time": "10:45 AM", "duration": "12 min", "fine": 3500, "status": "Pending", "severity": "High"},
        {"type": "No Parking Zone", "location": "Fort Station", "date": "Nov 28, 2024", "time": "2:30 PM", "duration": "8 min", "fine": 2000, "status": "Paid", "severity": "Medium"},
        {"type": "Double Parking", "location": "Borella Junction", "date": "Nov 15, 2024", "time": "9:15 AM", "duration": "25 min", "fine": 5500, "status": "Paid", "severity": "High"},
    ]
    
    if status_filter != "All":
        violations = [v for v in violations if v['status'] == status_filter]
    
    for v in violations:
        st.markdown(get_violation_card_html(
            v['type'],
            v['location'],
            f"{v['date']} • {v['time']}",
            v['fine'],
            v['status']
        ), unsafe_allow_html=True)
        
        if v['status'] == "Pending":
            if st.button(f"💳 PAY LKR {v['fine']:,}", key=f"pay_{v['date']}", use_container_width=True):
                st.session_state.show_payment = v
                st.rerun()
    
    # Payment Modal
    if st.session_state.get('show_payment'):
        v = st.session_state.show_payment
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(145deg, rgba(20, 20, 20, 0.98), rgba(10, 10, 10, 0.99));
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 1.5rem;
            margin-top: 1rem;
        ">
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <div style="font-family: 'Rajdhani', sans-serif; font-size: 1rem; color: #888; text-transform: uppercase; letter-spacing: 1px;">
                    Amount Due
                </div>
                <div style="font-family: 'Orbitron', sans-serif; font-size: 2.5rem; color: #ffffff; margin-top: 0.5rem;">
                    LKR {v['fine']:,}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Select Payment Method")
        
        payment_method = st.radio(
            "Payment Method",
            ["💳 Credit/Debit Card", "📱 EZ Cash", "🏦 Bank Transfer", "🌐 Online Banking"],
            label_visibility="collapsed"
        )
        
        if "Card" in payment_method:
            st.text_input("Card Number", placeholder="1234 5678 9012 3456")
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Expiry", placeholder="MM/YY")
            with col2:
                st.text_input("CVV", placeholder="123", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ CANCEL", use_container_width=True):
                st.session_state.show_payment = None
                st.rerun()
        with col2:
            if st.button("✅ CONFIRM PAYMENT", type="primary", use_container_width=True):
                with st.spinner("Processing..."):
                    import time
                    time.sleep(2)
                st.balloons()
                st.success("✅ Payment Successful!")
                st.session_state.show_payment = None


# ============================================================================
# 🚗 VEHICLES TAB
# ============================================================================
def show_vehicles_tab():
    """Show registered vehicles - Monochrome"""
    
    st.markdown("""
    <div style="
        font-family: 'Orbitron', sans-serif;
        font-size: 1.25rem;
        color: #ffffff;
        margin-bottom: 1.5rem;
        letter-spacing: 2px;
    ">MY VEHICLES</div>
    """, unsafe_allow_html=True)
    
    vehicles = [
        {"plate": "CAB-1234", "type": "Car", "color": "White", "make": "Toyota Aqua", "violations": 3},
        {"plate": "WP-5678", "type": "Motorcycle", "color": "Black", "make": "Honda CB350", "violations": 0},
    ]
    
    for v in vehicles:
        st.markdown(f"""
        <div class="vehicle-card">
            <div class="vehicle-plate">{v['plate']}</div>
            <div class="vehicle-info">
                <div class="vehicle-info-item">
                    <strong>Type</strong>
                    {v['type']}
                </div>
                <div class="vehicle-info-item">
                    <strong>Color</strong>
                    {v['color']}
                </div>
                <div class="vehicle-info-item">
                    <strong>Make</strong>
                    {v['make']}
                </div>
                <div class="vehicle-info-item">
                    <strong>Violations</strong>
                    {v['violations']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("➕ Add New Vehicle"):
        new_plate = st.text_input("License Plate", placeholder="e.g., ABC-1234")
        new_type = st.selectbox("Vehicle Type", ["Car", "Motorcycle", "Van", "TukTuk", "Bus", "Truck"])
        new_color = st.text_input("Color", placeholder="e.g., Silver")
        new_make = st.text_input("Make & Model", placeholder="e.g., Honda Civic")
        
        if st.button("➕ ADD VEHICLE", use_container_width=True):
            if new_plate:
                st.success(f"✅ Vehicle {new_plate} added successfully!")
            else:
                st.error("Please enter license plate")


# ============================================================================
# 👤 PROFILE TAB
# ============================================================================
def show_profile_tab():
    """Show user profile - Monochrome"""
    
    user = st.session_state.user
    
    st.markdown(get_profile_header_html(
        user['name'],
        user['email'],
        user['name'][0].upper()
    ), unsafe_allow_html=True)
    
    # Stats Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", f"{user.get('score', 85)}")
    with col2:
        st.metric("Violations", "3")
    with col3:
        st.metric("Warnings", "12")
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Account Details
    st.markdown("""
    <div style="
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        color: #ffffff;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    ">Account Details</div>
    """, unsafe_allow_html=True)
    
    details = [
        ("📧 Email", user['email']),
        ("📱 Phone", user['phone']),
        ("📅 Member Since", user.get('member_since', 'Jan 2024')),
        ("🏆 Badge", "Responsible Driver"),
    ]
    
    for label, value in details:
        st.markdown(f"""
        <div style="
            display: flex;
            justify-content: space-between;
            padding: 0.75rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        ">
            <span style="color: #888;">{label}</span>
            <span style="color: #e0e0e0;">{value}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Notification Settings
    st.markdown("""
    <div style="
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        color: #ffffff;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    ">Notification Settings</div>
    """, unsafe_allow_html=True)
    
    st.toggle("📍 Location-based Warnings", value=True)
    st.toggle("💸 Fine Reminders", value=True)
    st.toggle("📊 Weekly Score Reports", value=False)
    st.toggle("📢 Promotional Messages", value=False)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    st.markdown("### Audio Test")
    if st.button("🔊 Test Voice Warning"):
        play_voice_warning("This is a test of the driver warning system.")
        st.success("Playing test audio...")
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    if st.button("🚪 LOGOUT", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()


# ============================================================================
# 🎬 MAIN APPLICATION
# ============================================================================
def main():
    """Main application entry point"""
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'show_payment' not in st.session_state:
        st.session_state.show_payment = None
    
    if not st.session_state.logged_in:
        show_login()
    else:
        # Top Bar
        user = st.session_state.user
        st.markdown(f"""
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
            margin-bottom: 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        ">
            <div>
                <div style="font-family: 'Orbitron', sans-serif; font-size: 1.1rem; color: #ffffff; letter-spacing: 2px;">
                    SAFEDRIVE
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.85rem; color: #ffffff;">{user['name']}</div>
                <div style="font-size: 0.7rem; color: #666;">Score: {user.get('score', 85)}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Tab Navigation
        tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📋 Violations", "🚗 Vehicles", "👤 Profile"])
        
        with tab1:
            show_home_tab()
        
        with tab2:
            show_violations_tab()
        
        with tab3:
            show_vehicles_tab()
        
        with tab4:
            show_profile_tab()
        
        # Bottom gradient fade
        st.markdown("""
        <div style="
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 100px;
            background: linear-gradient(transparent, rgba(0,0,0,0.8));
            pointer-events: none;
            z-index: 100;
        "></div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()