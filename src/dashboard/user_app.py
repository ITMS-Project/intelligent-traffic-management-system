"""
Parking Violation User App
Mobile-responsive interface for vehicle owners
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Mobile-optimized configuration
st.set_page_config(
    page_title="Traffic Violations",
    page_icon="🚗",
    layout="centered",  # Better for mobile
    initial_sidebar_state="collapsed"  # Hide sidebar on mobile
)

# Custom CSS for mobile-responsive design
st.markdown("""
<style>
    /* Mobile-first design */
    .main {
        padding: 0.5rem;
    }
    
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .app-title {
        font-size: 1.8rem;
        font-weight: bold;
        margin: 0;
    }
    
    .app-subtitle {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.3rem;
    }
    
    .violation-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #ff6b6b;
    }
    
    .violation-card.paid {
        border-left-color: #51cf66;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .status-pending {
        background: #ffe3e3;
        color: #c92a2a;
    }
    
    .status-paid {
        background: #d3f9d8;
        color: #2b8a3e;
    }
    
    .status-warning {
        background: #fff3bf;
        color: #e67700;
    }
    
    .notification-alert {
        background: #fff3bf;
        border-left: 4px solid #fab005;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .stat-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #868e96;
        margin-top: 0.3rem;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state for user data"""
    if 'registered' not in st.session_state:
        st.session_state.registered = False
    if 'license_plate' not in st.session_state:
        st.session_state.license_plate = None
    if 'violations' not in st.session_state:
        st.session_state.violations = []
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []


def generate_mock_violations(license_plate):
    """Generate mock violation data for demo"""
    violations = [
        {
            'id': 'VIO-2025-001',
            'date': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M'),
            'location': 'Baseline Junction - Near Bus Stop',
            'duration': '8 minutes',
            'severity': 'HIGH',
            'fine_amount': 2500,
            'impact_score': 78,
            'vehicles_delayed': 12,
            'status': 'PENDING',
            'image_available': True,
            'payment_deadline': (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        },
        {
            'id': 'VIO-2025-002',
            'date': (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d %H:%M'),
            'location': 'Kanaththa Junction - Main Road',
            'duration': '3 minutes',
            'severity': 'MODERATE',
            'fine_amount': 1000,
            'impact_score': 45,
            'vehicles_delayed': 5,
            'status': 'PAID',
            'image_available': True,
            'payment_deadline': None
        },
        {
            'id': 'VIO-2025-003',
            'date': (datetime.now() - timedelta(hours=12)).strftime('%Y-%m-%d %H:%M'),
            'location': 'Baseline Junction - Corner',
            'duration': '15 minutes',
            'severity': 'SEVERE',
            'fine_amount': 5000,
            'impact_score': 92,
            'vehicles_delayed': 25,
            'status': 'PENDING',
            'image_available': True,
            'payment_deadline': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        }
    ]
    
    return violations


def generate_mock_notifications():
    """Generate mock notifications"""
    notifications = [
        {
            'type': 'WARNING',
            'title': 'Parking Violation Detected',
            'message': 'Your vehicle is parked in a no-parking zone at Baseline Junction',
            'time': '2 hours ago',
            'action_required': True
        },
        {
            'type': 'INFO',
            'title': 'Payment Reminder',
            'message': 'Fine payment due in 3 days for violation VIO-2025-001',
            'time': '5 hours ago',
            'action_required': True
        },
        {
            'type': 'SUCCESS',
            'title': 'Payment Confirmed',
            'message': 'Your payment for VIO-2025-002 has been processed',
            'time': '2 days ago',
            'action_required': False
        }
    ]
    
    return notifications


def show_registration_page():
    """Display registration page"""
    st.markdown('<div class="app-header"><div class="app-title">🚗 Vehicle Registration</div><div class="app-subtitle">Register to receive violation alerts</div></div>', unsafe_allow_html=True)
    
    st.write("")
    st.write("**Welcome to Smart Traffic Management**")
    st.write("Register your vehicle to:")
    st.write("✅ Receive real-time parking violation alerts")
    st.write("✅ Get early warnings before violations")
    st.write("✅ View and pay fines online")
    st.write("✅ Track your violation history")
    
    st.write("")
    st.write("---")
    
    with st.form("registration_form"):
        st.subheader("📝 Register Your Vehicle")
        
        license_plate = st.text_input(
            "License Plate Number",
            placeholder="ABC-1234",
            help="Enter your vehicle's license plate number"
        )
        
        phone = st.text_input(
            "Mobile Number",
            placeholder="+94 77 123 4567",
            help="For SMS alerts"
        )
        
        email = st.text_input(
            "Email Address (Optional)",
            placeholder="yourname@example.com"
        )
        
        agree = st.checkbox("I agree to receive violation notifications")
        
        submit = st.form_submit_button("🚀 Register Now")
        
        if submit:
            if license_plate and phone and agree:
                st.session_state.registered = True
                st.session_state.license_plate = license_plate.upper()
                st.session_state.violations = generate_mock_violations(license_plate)
                st.session_state.notifications = generate_mock_notifications()
                st.success(f"✅ Registration successful! Welcome, {license_plate.upper()}")
                st.balloons()
                st.rerun()
            else:
                st.error("⚠️ Please fill all required fields and agree to terms")


def show_home_page():
    """Display main home page with violations"""
    # Header
    st.markdown(f'<div class="app-header"><div class="app-title">🚗 My Traffic App</div><div class="app-subtitle">{st.session_state.license_plate}</div></div>', unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "⚠️ Violations", "🔔 Notifications", "👤 Profile"])
    
    with tab1:
        show_home_tab()
    
    with tab2:
        show_violations_tab()
    
    with tab3:
        show_notifications_tab()
    
    with tab4:
        show_profile_tab()


def show_home_tab():
    """Home tab with summary"""
    st.write("")
    
    # Summary statistics
    total_violations = len(st.session_state.violations)
    pending_violations = len([v for v in st.session_state.violations if v['status'] == 'PENDING'])
    total_fines = sum([v['fine_amount'] for v in st.session_state.violations if v['status'] == 'PENDING'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="stat-box"><div class="stat-value">{total_violations}</div><div class="stat-label">Total Violations</div></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="stat-box"><div class="stat-value">{pending_violations}</div><div class="stat-label">Pending</div></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'<div class="stat-box"><div class="stat-value">Rs. {total_fines:,}</div><div class="stat-label">Due Amount</div></div>', unsafe_allow_html=True)
    
    st.write("")
    
    # Recent activity
    if pending_violations > 0:
        st.markdown('<div class="notification-alert">⚠️ <strong>Action Required:</strong> You have pending violations. Please review and pay before the deadline.</div>', unsafe_allow_html=True)
    else:
        st.success("✅ No pending violations. Drive safe!")
    
    st.write("")
    st.subheader("📊 Recent Activity")
    
    # Show latest violation
    if st.session_state.violations:
        latest = st.session_state.violations[0]
        
        status_class = "status-pending" if latest['status'] == 'PENDING' else "status-paid"
        
        st.markdown(f"""
        <div class="violation-card {'paid' if latest['status'] == 'PAID' else ''}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <strong>{latest['id']}</strong>
                <span class="status-badge {status_class}">{latest['status']}</span>
            </div>
            <div style="color: #868e96; font-size: 0.9rem; margin-bottom: 0.5rem;">
                📍 {latest['location']}
            </div>
            <div style="color: #868e96; font-size: 0.9rem; margin-bottom: 0.5rem;">
                🕐 {latest['date']} • Duration: {latest['duration']}
            </div>
            <div style="font-size: 1.2rem; font-weight: bold; color: #667eea; margin-top: 0.8rem;">
                Rs. {latest['fine_amount']:,}
            </div>
        </div>
        """, unsafe_allow_html=True)


def show_violations_tab():
    """Violations tab with full list"""
    st.write("")
    st.subheader("⚠️ All Violations")
    
    if not st.session_state.violations:
        st.info("🎉 No violations found. Keep up the good driving!")
        return
    
    # Filter
    filter_status = st.selectbox("Filter by Status", ["All", "PENDING", "PAID"])
    
    violations = st.session_state.violations
    if filter_status != "All":
        violations = [v for v in violations if v['status'] == filter_status]
    
    st.write(f"**Showing {len(violations)} violation(s)**")
    st.write("")
    
    for violation in violations:
        with st.expander(f"🚗 {violation['id']} - {violation['location']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**📅 Date:** {violation['date']}")
                st.write(f"**📍 Location:** {violation['location']}")
                st.write(f"**⏱️ Duration:** {violation['duration']}")
                st.write(f"**🚨 Severity:** {violation['severity']}")
                st.write(f"**📊 Impact Score:** {violation['impact_score']}/100")
                st.write(f"**🚙 Vehicles Delayed:** {violation['vehicles_delayed']}")
                
                if violation['status'] == 'PENDING':
                    st.write(f"**⏰ Payment Deadline:** {violation['payment_deadline']}")
            
            with col2:
                st.metric("Fine Amount", f"Rs. {violation['fine_amount']:,}")
                
                if violation['status'] == 'PENDING':
                    if st.button(f"💳 Pay Now", key=f"pay_{violation['id']}"):
                        st.success("Payment processed! (Demo)")
                        st.balloons()
                else:
                    st.success("✅ Paid")
            
            st.write("")
            st.write("**🖼️ Violation Evidence:**")
            st.info("📸 Photo evidence available (Demo mode - image not shown)")


def show_notifications_tab():
    """Notifications tab"""
    st.write("")
    st.subheader("🔔 Notifications")
    
    if not st.session_state.notifications:
        st.info("📭 No new notifications")
        return
    
    for notif in st.session_state.notifications:
        if notif['type'] == 'WARNING':
            icon = "⚠️"
            bg_color = "#fff3bf"
        elif notif['type'] == 'INFO':
            icon = "ℹ️"
            bg_color = "#d3f9f8"
        else:
            icon = "✅"
            bg_color = "#d3f9d8"
        
        st.markdown(f"""
        <div style="background: {bg_color}; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">{icon}</span>
                <strong>{notif['title']}</strong>
            </div>
            <div style="margin-left: 2rem; color: #495057;">
                {notif['message']}
            </div>
            <div style="margin-left: 2rem; margin-top: 0.5rem; font-size: 0.85rem; color: #868e96;">
                {notif['time']}
            </div>
        </div>
        """, unsafe_allow_html=True)


def show_profile_tab():
    """Profile tab"""
    st.write("")
    st.subheader("👤 Profile Settings")
    
    st.write(f"**🚗 License Plate:** {st.session_state.license_plate}")
    st.write(f"**📊 Total Violations:** {len(st.session_state.violations)}")
    st.write(f"**📅 Member Since:** {datetime.now().strftime('%B %Y')}")
    
    st.write("")
    st.write("---")
    
    st.write("**⚙️ Settings**")
    
    st.checkbox("📧 Email notifications", value=True)
    st.checkbox("📱 SMS alerts", value=True)
    st.checkbox("🔔 Push notifications", value=True)
    
    st.write("")
    st.write("---")
    
    if st.button("🚪 Logout", type="primary"):
        st.session_state.registered = False
        st.session_state.license_plate = None
        st.session_state.violations = []
        st.session_state.notifications = []
        st.success("Logged out successfully!")
        st.rerun()


def main():
    """Main app function"""
    initialize_session_state()
    
    if not st.session_state.registered:
        show_registration_page()
    else:
        show_home_page()


if __name__ == "__main__":
    main()