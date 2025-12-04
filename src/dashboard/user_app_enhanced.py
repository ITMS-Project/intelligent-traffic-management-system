"""
📱 MOBILE DRIVER APP - Premium Futuristic Design
Intelligent Traffic Management System

Features:
- Real-Time Predictive Warnings (NOVELTY)
- Violation Notifications
- Driver Safety Score (100 points)
- Violation History
- Fine Payment Integration
- Profile & Vehicle Management
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
from pathlib import Path
import time
import plotly.graph_objects as go

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.database import db, user_ops, vehicle_ops, violation_ops
from src.dashboard.styles import (
    MOBILE_CSS,
    get_mobile_header_html,
    get_score_card_html,
    get_violation_card_html,
    get_vehicle_card_html,
    get_warning_banner_html,
    get_profile_header_html,
    SEVERITY_COLORS,
    STATUS_COLORS
)

# ============================================================================
# 🎯 PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Safe Drive",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply Premium CSS
st.markdown(MOBILE_CSS, unsafe_allow_html=True)


# ============================================================================
# 🔧 SESSION STATE INITIALIZATION
# ============================================================================
def init_session_state():
    """Initialize session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'db_connected' not in st.session_state:
        try:
            db.connect()
            st.session_state.db_connected = True
        except:
            st.session_state.db_connected = False


# ============================================================================
# 🔐 AUTHENTICATION
# ============================================================================
def show_login_page():
    """Display login/register page"""
    
    # App header
    st.markdown(get_mobile_header_html("SAFE DRIVE", "Driver Assistant"), unsafe_allow_html=True)
    
    # Login/Register tabs
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            
            st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
            
            submit = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if submit:
                if email and password:
                    # Demo login - accept any credentials
                    st.session_state.logged_in = True
                    st.session_state.user = {
                        'id': 'demo_user',
                        'username': email.split('@')[0],
                        'email': email,
                        'full_name': email.split('@')[0].title(),
                        'phone': '+94 77 123 4567',
                        'safety_score': 85,
                        'score_badge': 'Good',
                        'total_violations': 3,
                        'total_warnings': 5
                    }
                    st.rerun()
                else:
                    st.error("Please enter your email and password")
        
        # Demo login button
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.85rem;">
            Demo credentials: any email/password
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name", placeholder="John")
            with col2:
                last_name = st.text_input("Last Name", placeholder="Doe")
            
            reg_email = st.text_input("Email", placeholder="your@email.com", key="reg_email")
            phone = st.text_input("Phone", placeholder="+94 77 123 4567")
            reg_password = st.text_input("Password", type="password", placeholder="••••••••", key="reg_pass")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••")
            
            st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
            
            # Vehicle registration
            st.markdown("#### 🚗 Vehicle Details (Optional)")
            col1, col2 = st.columns(2)
            with col1:
                license_plate = st.text_input("License Plate", placeholder="WP CAB-1234")
            with col2:
                vehicle_type = st.selectbox("Vehicle Type", ["Car", "Motorcycle", "TukTuk", "Van", "Jeep"])
            
            register = st.form_submit_button("📝 Register", use_container_width=True)
            
            if register:
                if all([first_name, last_name, reg_email, phone, reg_password]):
                    if reg_password == confirm_password:
                        st.success("✅ Registration successful! Please login.")
                    else:
                        st.error("Passwords don't match!")
                else:
                    st.error("Please fill all required fields")


# ============================================================================
# 🏠 HOME TAB
# ============================================================================
def show_home_tab():
    """Display home tab with safety score and warnings"""
    
    user = st.session_state.user
    
    # Check for active warnings (demo)
    has_warning = True
    
    if has_warning:
        st.markdown(f"""
        <div class="warning-banner">
            <div class="warning-title">⚠️ ACTIVE WARNING</div>
            <div class="warning-message">
                You are approaching a no-parking zone at <strong>Pettah Market</strong>. 
                Please find an authorized parking area to avoid a fine.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ I've Moved", use_container_width=True):
                st.success("Great! Warning cleared. +3 safety points!")
                time.sleep(1)
                st.rerun()
        with col2:
            if st.button("🗺️ Find Parking", use_container_width=True):
                st.info("Opening maps...")
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Safety Score Card
    st.markdown(get_score_card_html(user['safety_score'], user['score_badge']), unsafe_allow_html=True)
    
    # Quick Stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Violations", str(user['total_violations']))
    with col2:
        pending_fines = 7500  # Demo value
        st.metric("Pending Fines", f"LKR {pending_fines:,}")
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Score History Chart
    st.markdown("""
    <div style="font-family: 'Rajdhani', sans-serif; font-size: 1rem; color: white; margin-bottom: 1rem;">
        📈 Score History (30 Days)
    </div>
    """, unsafe_allow_html=True)
    
    # Generate score history data
    import numpy as np
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    scores = np.clip(np.cumsum(np.random.randn(30) * 2) + 85, 0, 100).astype(int)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=scores,
        mode='lines+markers',
        line=dict(color='#00ff88', width=2),
        marker=dict(size=6, color='#00ff88'),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 136, 0.1)',
        hovertemplate='<b>%{x|%b %d}</b><br>Score: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(10, 10, 15, 0.8)',
        plot_bgcolor='rgba(10, 10, 15, 0.8)',
        font=dict(color='#888'),
        xaxis=dict(
            showgrid=False,
            showticklabels=True,
            tickformat='%b %d',
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            range=[0, 100],
            tickfont=dict(size=10)
        ),
        margin=dict(t=10, b=30, l=40, r=10),
        height=200,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown("""
    <div style="font-family: 'Rajdhani', sans-serif; font-size: 1rem; color: white; margin-bottom: 1rem;">
        🕐 Recent Activity
    </div>
    """, unsafe_allow_html=True)
    
    activities = [
        {"type": "warning", "text": "Warning received - Pettah Market", "time": "2 min ago", "icon": "⚠️"},
        {"type": "violation", "text": "Violation - Fort Station (Paid)", "time": "2 days ago", "icon": "🚗"},
        {"type": "score", "text": "Safety score increased +5", "time": "3 days ago", "icon": "📈"},
    ]
    
    for activity in activities:
        color = "#f59e0b" if activity['type'] == 'warning' else "#00ff88" if activity['type'] == 'score' else "#00d4ff"
        st.markdown(f"""
        <div style="
            background: rgba(15, 15, 20, 0.8);
            border-left: 3px solid {color};
            border-radius: 0 8px 8px 0;
            padding: 0.75rem 1rem;
            margin-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="font-size: 1.25rem;">{activity['icon']}</span>
                <span style="color: white; font-size: 0.85rem;">{activity['text']}</span>
            </div>
            <span style="color: #666; font-size: 0.75rem;">{activity['time']}</span>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# 📜 VIOLATIONS TAB
# ============================================================================
def show_violations_tab():
    """Display violations list with payment option"""
    
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h3 style="font-family: 'Orbitron', sans-serif; color: white; margin: 0; font-size: 1.2rem;">
            📜 My Violations
        </h3>
        <p style="color: #666; font-size: 0.8rem; margin-top: 0.25rem;">View and pay your parking fines</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter
    filter_option = st.selectbox("Filter", ["All", "Pending", "Paid"], label_visibility="collapsed")
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Sample violations
    violations = [
        {
            "id": "VIO-001",
            "type": "Illegal Parking",
            "location": "Pettah Market",
            "date": "Dec 1, 2025",
            "time": "10:45 AM",
            "duration": "12 min",
            "fine": 3500,
            "status": "Pending",
            "severity": "High"
        },
        {
            "id": "VIO-002",
            "type": "No Parking Zone",
            "location": "Fort Station",
            "date": "Nov 28, 2025",
            "time": "2:30 PM",
            "duration": "8 min",
            "fine": 2500,
            "status": "Paid",
            "severity": "Medium"
        },
        {
            "id": "VIO-003",
            "type": "Bus Lane Parking",
            "location": "Maradana",
            "date": "Nov 25, 2025",
            "time": "9:15 AM",
            "duration": "5 min",
            "fine": 4000,
            "status": "Pending",
            "severity": "High"
        }
    ]
    
    # Filter violations
    if filter_option != "All":
        violations = [v for v in violations if v['status'] == filter_option]
    
    # Display violations
    for violation in violations:
        status_color = "#00ff88" if violation['status'] == "Paid" else "#f59e0b"
        severity_color = SEVERITY_COLORS.get(violation['severity'].lower(), "#f59e0b")
        card_class = "paid" if violation['status'] == "Paid" else ""
        
        st.markdown(f"""
        <div class="violation-card {card_class}">
            <div class="violation-header">
                <div class="violation-type">{violation['type']}</div>
                <div class="violation-status {'paid' if violation['status'] == 'Paid' else 'pending'}">
                    {violation['status']}
                </div>
            </div>
            <div class="violation-details">
                <div class="violation-detail">📍 <span>{violation['location']}</span></div>
                <div class="violation-detail">📅 <span>{violation['date']}</span></div>
                <div class="violation-detail">🕐 <span>{violation['time']}</span></div>
                <div class="violation-detail">⏱️ <span>{violation['duration']}</span></div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem;">
                <span style="font-size: 0.75rem; color: {severity_color};">● {violation['severity']} Severity</span>
                <div class="violation-fine">LKR {violation['fine']:,}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Pay button for pending violations
        if violation['status'] == "Pending":
            if st.button(f"💳 Pay LKR {violation['fine']:,}", key=f"pay_{violation['id']}", use_container_width=True):
                show_payment_modal(violation)


def show_payment_modal(violation):
    """Show payment options"""
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, rgba(15, 15, 20, 0.98), rgba(5, 5, 10, 0.99));
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
    ">
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <div style="font-size: 0.85rem; color: #888; text-transform: uppercase; letter-spacing: 1px;">
                Amount to Pay
            </div>
            <div style="font-family: 'Orbitron', sans-serif; font-size: 2.5rem; color: white; margin-top: 0.5rem;">
                <span style="font-size: 1rem; color: #666;">LKR</span> {violation['fine']:,}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Select Payment Method")
    
    payment_method = st.radio(
        "Payment Method",
        ["💳 Credit/Debit Card", "📱 EZ Cash", "🏦 Bank Transfer", "💰 Online Banking"],
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    if "Card" in payment_method:
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Card Number", placeholder="1234 5678 9012 3456")
        with col2:
            st.text_input("CVV", placeholder="123", type="password")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Expiry Date", placeholder="MM/YY")
        with col2:
            st.text_input("Name on Card", placeholder="JOHN DOE")
    
    if st.button("✅ Confirm Payment", type="primary", use_container_width=True):
        with st.spinner("Processing payment..."):
            time.sleep(2)
        st.balloons()
        st.success("✅ Payment Successful! Thank you.")
        time.sleep(1)
        st.rerun()


# ============================================================================
# 🚗 VEHICLES TAB
# ============================================================================
def show_vehicles_tab():
    """Display registered vehicles"""
    
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h3 style="font-family: 'Orbitron', sans-serif; color: white; margin: 0; font-size: 1.2rem;">
            🚗 My Vehicles
        </h3>
        <p style="color: #666; font-size: 0.8rem; margin-top: 0.25rem;">Manage your registered vehicles</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample vehicles
    vehicles = [
        {"plate": "WP CAB-1234", "type": "Car", "color": "Silver", "make": "Toyota Axio", "violations": 2},
        {"plate": "WP ABC-5678", "type": "Motorcycle", "color": "Black", "make": "Honda CB350", "violations": 1},
    ]
    
    for vehicle in vehicles:
        st.markdown(f"""
        <div class="vehicle-card">
            <div class="vehicle-plate">{vehicle['plate']}</div>
            <div class="vehicle-info">
                <div class="vehicle-info-item">
                    <strong>Type</strong>
                    {vehicle['type']}
                </div>
                <div class="vehicle-info-item">
                    <strong>Color</strong>
                    {vehicle['color']}
                </div>
                <div class="vehicle-info-item">
                    <strong>Make/Model</strong>
                    {vehicle['make']}
                </div>
                <div class="vehicle-info-item">
                    <strong>Violations</strong>
                    <span style="color: {'#ef4444' if vehicle['violations'] > 0 else '#00ff88'};">
                        {vehicle['violations']}
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Add vehicle form
    with st.expander("➕ Add New Vehicle"):
        with st.form("add_vehicle_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_plate = st.text_input("License Plate", placeholder="WP XXX-0000")
            with col2:
                new_type = st.selectbox("Vehicle Type", ["Car", "Motorcycle", "TukTuk", "Van", "Jeep", "Bus"])
            
            col1, col2 = st.columns(2)
            with col1:
                new_color = st.text_input("Color", placeholder="Silver")
            with col2:
                new_make = st.text_input("Make/Model", placeholder="Toyota Axio")
            
            submit = st.form_submit_button("➕ Add Vehicle", use_container_width=True)
            
            if submit:
                if new_plate and new_type:
                    st.success(f"✅ Vehicle {new_plate} added successfully!")
                else:
                    st.error("Please fill required fields")


# ============================================================================
# 👤 PROFILE TAB
# ============================================================================
def show_profile_tab():
    """Display user profile and settings"""
    
    user = st.session_state.user
    
    # Profile header
    st.markdown(get_profile_header_html(
        user['full_name'],
        user['email'],
        user['full_name'][0].upper()
    ), unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Stats row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", str(user['safety_score']))
    with col2:
        st.metric("Violations", str(user['total_violations']))
    with col3:
        st.metric("Warnings", str(user['total_warnings']))
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Account details
    st.markdown("""
    <div style="font-family: 'Rajdhani', sans-serif; font-size: 1rem; color: white; margin-bottom: 1rem;">
        📋 Account Details
    </div>
    """, unsafe_allow_html=True)
    
    details = [
        ("📧 Email", user['email']),
        ("📱 Phone", user['phone']),
        ("🎫 Member Since", "October 2025"),
        ("🏆 Badge", user['score_badge']),
    ]
    
    for label, value in details:
        st.markdown(f"""
        <div style="
            background: rgba(15, 15, 20, 0.8);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <span style="color: #888; font-size: 0.9rem;">{label}</span>
            <span style="color: white; font-size: 0.9rem;">{value}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Notification settings
    st.markdown("""
    <div style="font-family: 'Rajdhani', sans-serif; font-size: 1rem; color: white; margin-bottom: 1rem;">
        🔔 Notification Settings
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.toggle("Push Notifications", value=True)
        st.toggle("Warning Alerts", value=True)
    with col2:
        st.toggle("Violation Alerts", value=True)
        st.toggle("Payment Reminders", value=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Logout button
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()


# ============================================================================
# 🎬 MAIN APPLICATION
# ============================================================================
def main():
    """Main application entry point"""
    
    # Initialize session state
    init_session_state()
    
    # Check if logged in
    if not st.session_state.logged_in:
        show_login_page()
        return
    
    # App header for logged in users
    user = st.session_state.user
    
    st.markdown(f"""
    <div style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 1rem;
    ">
        <div>
            <div style="font-family: 'Orbitron', sans-serif; font-size: 1.1rem; color: white; letter-spacing: 2px;">
                SAFE DRIVE
            </div>
            <div style="font-size: 0.75rem; color: #00ff88;">● Online</div>
        </div>
        <div style="text-align: right;">
            <div style="color: white; font-size: 0.9rem;">{user['full_name']}</div>
            <div style="font-size: 0.75rem; color: #888;">Score: {user['safety_score']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📜 Violations", "🚗 Vehicles", "👤 Profile"])
    
    with tab1:
        show_home_tab()
    
    with tab2:
        show_violations_tab()
    
    with tab3:
        show_vehicles_tab()
    
    with tab4:
        show_profile_tab()
    
    # Bottom navigation bar (visual only)
    st.markdown("""
    <div style="
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.9) 50%);
        padding: 2rem 1rem 1rem;
        pointer-events: none;
    "></div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()