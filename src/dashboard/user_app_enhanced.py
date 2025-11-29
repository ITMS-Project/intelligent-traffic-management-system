"""
Enhanced Parking Violation User App
Mobile-responsive interface with MongoDB integration and authentication
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.database import db, user_ops, vehicle_ops, violation_ops

# Mobile-optimized configuration
st.set_page_config(
    page_title="Traffic Violations",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-responsive design
st.markdown("""
<style>
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

    .status-reviewed {
        background: #d0ebff;
        color: #1864ab;
    }

    .status-paid {
        background: #d3f9d8;
        color: #2b8a3e;
    }

    .status-dismissed {
        background: #e9ecef;
        color: #495057;
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


def initialize_database():
    """Initialize database connection"""
    if 'db_connected' not in st.session_state:
        try:
            db.connect()
            st.session_state.db_connected = True
        except Exception as e:
            st.error(f"❌ Database connection failed: {e}")
            st.session_state.db_connected = False


def initialize_session_state():
    """Initialize session state for user data"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None


def show_login_page():
    """Display login/registration page"""
    st.markdown(
        '<div class="app-header">'
        '<div class="app-title">🚗 Traffic Management</div>'
        '<div class="app-subtitle">Check Your Violations</div>'
        '</div>',
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    with tab1:
        show_login_form()

    with tab2:
        show_registration_form()


def show_login_form():
    """Display login form"""
    st.write("")
    st.write("**Welcome Back!**")

    with st.form("login_form"):
        email = st.text_input(
            "Email Address",
            placeholder="your.email@example.com"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        submit = st.form_submit_button("🔐 Login")

        if submit:
            if not st.session_state.get('db_connected'):
                st.error("❌ Database not connected. Cannot login.")
                return

            if email and password:
                # Verify credentials
                if user_ops.verify_password(email, password):
                    user = user_ops.get_user_by_email(email)
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.session_state.user_data = user
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password")
            else:
                st.error("⚠️ Please fill all fields")


def show_registration_form():
    """Display registration form"""
    st.write("")
    st.write("**Create New Account**")
    st.write("Register to receive violation alerts and manage your vehicles.")

    with st.form("registration_form"):
        col1, col2 = st.columns(2)

        with col1:
            username = st.text_input(
                "Username",
                placeholder="username",
                help="Choose a unique username"
            )

        with col2:
            email = st.text_input(
                "Email",
                placeholder="your.email@example.com"
            )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a strong password",
            help="Minimum 6 characters"
        )

        password_confirm = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter password"
        )

        st.write("")
        st.write("**Register Your Vehicle (Optional)**")

        license_plate = st.text_input(
            "License Plate Number",
            placeholder="ABC-1234",
            help="You can add vehicles later"
        )

        vehicle_type = st.selectbox(
            "Vehicle Type",
            ["parked_car", "parked_tuktuk", "parked_bus", "parked_van",
             "parked_truck", "parked_motorcycle", "parked_jeep"]
        )

        agree = st.checkbox("I agree to receive violation notifications")

        submit = st.form_submit_button("🚀 Register")

        if submit:
            if not st.session_state.get('db_connected'):
                st.error("❌ Database not connected. Cannot register.")
                return

            # Validation
            if not (username and email and password and agree):
                st.error("⚠️ Please fill all required fields and agree to terms")
                return

            if password != password_confirm:
                st.error("❌ Passwords do not match")
                return

            if len(password) < 6:
                st.error("❌ Password must be at least 6 characters")
                return

            try:
                # Create user
                user_id = user_ops.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role="viewer"
                )

                # Register vehicle if provided
                if license_plate:
                    vehicle_ops.register_vehicle(
                        license_plate=license_plate.upper(),
                        vehicle_type=vehicle_type
                    )

                st.success(f"✅ Registration successful! Welcome, {username}!")
                st.balloons()
                st.info("Please login with your credentials")

            except Exception as e:
                if "duplicate" in str(e).lower():
                    st.error("❌ Username or email already exists")
                else:
                    st.error(f"❌ Registration failed: {e}")


def show_home_page():
    """Display main home page with violations"""
    user = st.session_state.user_data

    # Header
    st.markdown(
        f'<div class="app-header">'
        f'<div class="app-title">🚗 My Violations</div>'
        f'<div class="app-subtitle">{user["username"]}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "⚠️ Violations", "🚗 Vehicles", "👤 Profile"])

    with tab1:
        show_home_tab()

    with tab2:
        show_violations_tab()

    with tab3:
        show_vehicles_tab()

    with tab4:
        show_profile_tab()


def show_home_tab():
    """Home tab with summary"""
    st.write("")

    if not st.session_state.get('db_connected'):
        st.warning("Database offline - cannot display information")
        return

    try:
        # Get user's vehicles
        user_vehicles = vehicle_ops.collection.find()
        vehicle_list = list(user_vehicles)

        # Get violations for all user vehicles
        all_violations = []
        for vehicle in vehicle_list:
            violations = violation_ops.get_violations_by_plate(vehicle['license_plate'])
            all_violations.extend(violations)

        # Calculate statistics
        total_violations = len(all_violations)
        pending_violations = len([v for v in all_violations if v['status'] == 'pending'])
        total_fines = sum([v['fine_amount'] for v in all_violations if v['status'] == 'pending'])

        # Display statistics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f'<div class="stat-box">'
                f'<div class="stat-value">{total_violations}</div>'
                f'<div class="stat-label">Total Violations</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f'<div class="stat-box">'
                f'<div class="stat-value">{pending_violations}</div>'
                f'<div class="stat-label">Pending</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f'<div class="stat-box">'
                f'<div class="stat-value">Rs. {total_fines:,.0f}</div>'
                f'<div class="stat-label">Due Amount</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        st.write("")

        # Recent activity
        if pending_violations > 0:
            st.markdown(
                '<div class="notification-alert">'
                '⚠️ <strong>Action Required:</strong> You have pending violations. '
                'Please review and pay before the deadline.'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            st.success("✅ No pending violations. Drive safe!")

        # Show recent violations
        if all_violations:
            st.write("")
            st.subheader("📊 Recent Activity")

            # Sort by timestamp
            all_violations.sort(key=lambda x: x['timestamp'], reverse=True)

            # Show latest 3
            for violation in all_violations[:3]:
                status_class = f"status-{violation['status']}"

                st.markdown(
                    f"""
                    <div class="violation-card {'paid' if violation['status'] == 'paid' else ''}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <strong>{violation.get('license_plate', 'Unknown')}</strong>
                            <span class="status-badge {status_class}">{violation['status'].upper()}</span>
                        </div>
                        <div style="color: #868e96; font-size: 0.9rem; margin-bottom: 0.5rem;">
                            📍 {violation['location']}
                        </div>
                        <div style="color: #868e96; font-size: 0.9rem; margin-bottom: 0.5rem;">
                            🕐 {violation['timestamp'].strftime('%Y-%m-%d %H:%M')}
                        </div>
                        <div style="font-size: 1.2rem; font-weight: bold; color: #667eea; margin-top: 0.8rem;">
                            Rs. {violation['fine_amount']:,.0f}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.error(f"Error loading home data: {e}")


def show_violations_tab():
    """Violations tab with full list"""
    st.write("")
    st.subheader("⚠️ All Violations")

    if not st.session_state.get('db_connected'):
        st.warning("Database offline")
        return

    try:
        # Get user's vehicles
        user_vehicles = vehicle_ops.collection.find()
        vehicle_list = list(user_vehicles)

        if not vehicle_list:
            st.info("🚗 No vehicles registered. Add a vehicle to see violations.")
            return

        # Get all violations
        all_violations = []
        for vehicle in vehicle_list:
            violations = violation_ops.get_violations_by_plate(vehicle['license_plate'])
            all_violations.extend(violations)

        if not all_violations:
            st.success("🎉 No violations found. Keep up the good driving!")
            return

        # Filter
        col1, col2 = st.columns(2)
        with col1:
            filter_status = st.selectbox(
                "Status",
                ["All", "pending", "reviewed", "paid", "dismissed"]
            )
        with col2:
            filter_vehicle = st.selectbox(
                "Vehicle",
                ["All"] + [v['license_plate'] for v in vehicle_list]
            )

        # Apply filters
        filtered = all_violations
        if filter_status != "All":
            filtered = [v for v in filtered if v['status'] == filter_status]
        if filter_vehicle != "All":
            filtered = [v for v in filtered if v.get('license_plate') == filter_vehicle]

        st.write(f"**Showing {len(filtered)} violation(s)**")
        st.write("")

        # Display violations
        for violation in filtered:
            status_class = f"status-{violation['status']}"

            with st.expander(
                f"🚗 {violation.get('license_plate', 'Unknown')} - "
                f"{violation['location']} - "
                f"Rs. {violation['fine_amount']:,.0f}",
                expanded=False
            ):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.write(f"**📅 Date:** {violation['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                    st.write(f"**📍 Location:** {violation['location']}")
                    st.write(f"**🚗 Vehicle Type:** {violation['vehicle_type']}")
                    st.write(f"**🚨 Severity:** {violation['severity'].upper()}")
                    st.write(f"**💰 Fine:** Rs. {violation['fine_amount']:,.0f}")
                    st.write(f"**📊 Confidence:** {violation['confidence']:.2%}")

                    if violation.get('notes'):
                        st.write(f"**📝 Notes:** {violation['notes']}")

                with col2:
                    st.markdown(
                        f'<span class="status-badge {status_class}">{violation["status"].upper()}</span>',
                        unsafe_allow_html=True
                    )

                    st.write("")

                    if violation['status'] == 'pending':
                        if st.button(f"💳 Pay Now", key=f"pay_{violation['_id']}"):
                            st.success("Payment feature coming soon!")
                            st.info("This is a demo. In production, this would integrate with a payment gateway.")

    except Exception as e:
        st.error(f"Error loading violations: {e}")


def show_vehicles_tab():
    """Vehicles management tab"""
    st.write("")
    st.subheader("🚗 My Vehicles")

    if not st.session_state.get('db_connected'):
        st.warning("Database offline")
        return

    try:
        # Get user's vehicles
        user_vehicles = vehicle_ops.collection.find()
        vehicle_list = list(user_vehicles)

        if vehicle_list:
            st.write(f"**You have {len(vehicle_list)} vehicle(s) registered**")
            st.write("")

            for vehicle in vehicle_list:
                with st.expander(
                    f"🚗 {vehicle['license_plate']} - {vehicle['vehicle_type'].replace('parked_', '').title()}",
                    expanded=True
                ):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(f"**Plate:** {vehicle['license_plate']}")
                        st.write(f"**Type:** {vehicle['vehicle_type'].replace('parked_', '').title()}")
                        if vehicle.get('color'):
                            st.write(f"**Color:** {vehicle['color']}")
                        if vehicle.get('make'):
                            st.write(f"**Make:** {vehicle['make']}")
                        if vehicle.get('model'):
                            st.write(f"**Model:** {vehicle['model']}")

                    with col2:
                        # Get violation count for this vehicle
                        violations = violation_ops.get_violations_by_plate(vehicle['license_plate'])
                        st.metric("Total Violations", len(violations))

        # Add new vehicle form
        st.write("")
        st.write("---")
        st.write("**➕ Add New Vehicle**")

        with st.form("add_vehicle_form"):
            col1, col2 = st.columns(2)

            with col1:
                new_plate = st.text_input("License Plate", placeholder="ABC-1234")
                new_type = st.selectbox(
                    "Vehicle Type",
                    ["parked_car", "parked_tuktuk", "parked_bus", "parked_van",
                     "parked_truck", "parked_motorcycle", "parked_jeep"]
                )

            with col2:
                new_color = st.text_input("Color (Optional)", placeholder="Red")
                new_make = st.text_input("Make (Optional)", placeholder="Toyota")

            new_model = st.text_input("Model (Optional)", placeholder="Corolla")

            submit = st.form_submit_button("➕ Add Vehicle")

            if submit:
                if new_plate and new_type:
                    try:
                        vehicle_ops.register_vehicle(
                            license_plate=new_plate.upper(),
                            vehicle_type=new_type,
                            color=new_color if new_color else None,
                            make=new_make if new_make else None,
                            model=new_model if new_model else None
                        )
                        st.success(f"✅ Vehicle {new_plate.upper()} added!")
                        st.rerun()
                    except Exception as e:
                        if "duplicate" in str(e).lower():
                            st.error("❌ This vehicle is already registered")
                        else:
                            st.error(f"❌ Error: {e}")
                else:
                    st.error("⚠️ Please fill required fields")

    except Exception as e:
        st.error(f"Error managing vehicles: {e}")


def show_profile_tab():
    """Profile tab"""
    st.write("")
    st.subheader("👤 Profile Settings")

    user = st.session_state.user_data

    st.write(f"**Username:** {user['username']}")
    st.write(f"**Email:** {user['email']}")
    st.write(f"**Role:** {user['role'].title()}")
    st.write(f"**Member Since:** {user['created_at'].strftime('%B %Y')}")

    st.write("")
    st.write("---")

    st.write("**⚙️ Notification Settings**")
    st.checkbox("📧 Email notifications", value=True)
    st.checkbox("📱 SMS alerts", value=True)
    st.checkbox("🔔 Push notifications", value=True)

    st.write("")
    st.write("---")

    if st.button("🚪 Logout", type="primary"):
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.session_state.user_data = None
        st.success("Logged out successfully!")
        st.rerun()


def main():
    """Main app function"""
    initialize_database()
    initialize_session_state()

    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_home_page()


if __name__ == "__main__":
    main()
