"""
Enhanced Parking Violation User App
Mobile-responsive interface with MongoDB integration and authentication
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.database import db, user_ops, vehicle_ops, violation_ops
from src.dashboard.styles import MOBILE_CSS

# Mobile-optimized configuration
st.set_page_config(
    page_title="Traffic App",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply Custom CSS
st.markdown(MOBILE_CSS, unsafe_allow_html=True)


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
        '<div class="app-title">TRAFFIC APP</div>'
        '<div class="app-subtitle">INTELLIGENT TRAFFIC CONTROL</div>'
        '</div>',
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(["LOGIN", "REGISTER"])

    with tab1:
        show_login_form()

    with tab2:
        show_registration_form()


def show_login_form():
    """Display login form"""
    st.write("")
    
    with st.container():
        st.write("### WELCOME BACK")
        st.write("Please authenticate to access your vehicle data.")
        st.write("")

        with st.form("login_form"):
            email = st.text_input(
                "Email Address",
                placeholder="name@example.com"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="••••••••"
            )

            st.write("")
            submit = st.form_submit_button("AUTHENTICATE")

            if submit:
                if not st.session_state.get('db_connected'):
                    st.error("❌ System Offline")
                    return

                if email and password:
                    # Verify credentials
                    if user_ops.verify_password(email, password):
                        user = user_ops.get_user_by_email(email)
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.user_data = user
                        st.success("✅ Access Granted")
                        st.rerun()
                    else:
                        st.error("❌ Access Denied")
                else:
                    st.error("⚠️ Credentials Required")


def show_registration_form():
    """Display registration form"""
    st.write("")
    st.write("### NEW USER REGISTRATION")

    with st.form("registration_form"):
        col1, col2 = st.columns(2)

        with col1:
            username = st.text_input("Username", placeholder="username")

        with col2:
            email = st.text_input("Email", placeholder="name@example.com")

        password = st.text_input("Password", type="password", placeholder="••••••••")
        password_confirm = st.text_input("Confirm Password", type="password", placeholder="••••••••")

        st.write("")
        st.write("**VEHICLE REGISTRATION (OPTIONAL)**")

        license_plate = st.text_input("License Plate", placeholder="ABC-1234")
        
        vehicle_type = st.selectbox(
            "Vehicle Type",
            ["parked_car", "parked_tuktuk", "parked_bus", "parked_van",
             "parked_truck", "parked_motorcycle", "parked_jeep"]
        )

        agree = st.checkbox("I agree to terms of service")

        st.write("")
        submit = st.form_submit_button("CREATE ACCOUNT")

        if submit:
            if not st.session_state.get('db_connected'):
                st.error("❌ System Offline")
                return

            if not (username and email and password and agree):
                st.error("⚠️ All fields required")
                return

            if password != password_confirm:
                st.error("❌ Passwords mismatch")
                return

            try:
                user_id = user_ops.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role="viewer"
                )

                if license_plate:
                    vehicle_ops.register_vehicle(
                        license_plate=license_plate.upper(),
                        vehicle_type=vehicle_type
                    )

                st.success(f"✅ Account Created! Welcome, {username}.")
                st.info("Please login to continue.")

            except Exception as e:
                if "duplicate" in str(e).lower():
                    st.error("❌ Account already exists")
                else:
                    st.error(f"❌ Error: {e}")


def show_home_page():
    """Display main home page with violations"""
    user = st.session_state.user_data

    # Header
    st.markdown(
        f'<div class="app-header">'
        f'<div class="app-title">DASHBOARD</div>'
        f'<div class="app-subtitle">{user["username"]}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["OVERVIEW", "MAP", "VIOLATIONS", "VEHICLES", "PROFILE"])

    with tab1:
        show_home_tab()

    with tab2:
        show_map_tab()

    with tab3:
        show_violations_tab()

    with tab4:
        show_vehicles_tab()

    with tab5:
        show_profile_tab()


def show_home_tab():
    """Home tab with summary"""
    st.write("")

    if not st.session_state.get('db_connected'):
        st.warning("System Offline")
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
            st.metric("Total", total_violations)
        with col2:
            st.metric("Pending", pending_violations)
        with col3:
            st.metric("Due (LKR)", f"{total_fines:,.0f}")

        st.write("---")

        # Recent activity
        if pending_violations > 0:
            st.warning("⚠️ ACTION REQUIRED: You have pending fines.")
        else:
            st.success("✅ STATUS CLEAR: No pending actions.")

        # Show recent violations
        if all_violations:
            st.write("### RECENT ACTIVITY")

            # Sort by timestamp
            all_violations.sort(key=lambda x: x['timestamp'], reverse=True)

            # Show latest 3
            for violation in all_violations[:3]:
                status_class = f"status-{violation['status']}"

                st.markdown(
                    f"""
                    <div class="violation-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <span style="font-weight: 700; font-size: 1.1rem;">{violation.get('license_plate', 'Unknown')}</span>
                            <span class="status-badge {status_class}">{violation['status']}</span>
                        </div>
                        <div style="color: #aaa; font-size: 0.8rem; margin-bottom: 0.5rem;">
                            {violation['location']} • {violation['timestamp'].strftime('%d %b %H:%M')}
                        </div>
                        <div style="font-size: 1.5rem; font-weight: 300; color: #2E86DE; margin-top: 0.5rem;">
                            LKR {violation['fine_amount']:,.0f}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.error(f"Error loading data: {e}")



def show_map_tab():
    """Display map with parking zones"""
    st.write("")
    st.write("### 🗺️ PARKING ZONES")
    
    # Mock data for map
    # Red = No Parking, Green = Allowed
    map_data = pd.DataFrame({
        'lat': [6.9271, 6.9275, 6.9265],
        'lon': [79.8612, 79.8618, 79.8605],
        'type': ['illegal', 'legal', 'legal'],
        'color': ['#FF0000', '#00FF00', '#00FF00']
    })
    
    st.map(map_data, zoom=15)
    
    st.info("🔴 Red: No Parking Zone | 🟢 Green: Allowed Parking")
    
    st.write("### 📡 LIVE ALERTS")
    if st.button("Simulate Zone Entry"):
        with st.spinner("Detecting location..."):
            time.sleep(1.5)
        
        st.error("⚠️ WARNING: YOU ARE ENTERING A NO-PARKING ZONE!")
        st.caption("Please move your vehicle immediately to avoid fines.")
        
        # Audio alert simulation (visual only for web)
        st.toast("🔊 Audio Alert: 'Warning, Illegal Parking Zone'")


def show_violations_tab():
    """Violations tab with full list"""
    st.write("")
    st.write("### VIOLATION HISTORY")

    if not st.session_state.get('db_connected'):
        st.warning("System Offline")
        return

    try:
        user_vehicles = vehicle_ops.collection.find()
        vehicle_list = list(user_vehicles)

        if not vehicle_list:
            st.info("No vehicles registered.")
            return

        all_violations = []
        for vehicle in vehicle_list:
            violations = violation_ops.get_violations_by_plate(vehicle['license_plate'])
            all_violations.extend(violations)

        if not all_violations:
            st.info("No violations found.")
            return

        # Display violations
        for violation in all_violations:
            status_class = f"status-{violation['status']}"

            with st.expander(
                f"{violation.get('license_plate')} • LKR {violation['fine_amount']:,.0f}",
                expanded=False
            ):
                st.write(f"**Date:** {violation['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                st.write(f"**Location:** {violation['location']}")
                st.write(f"**Type:** {violation['vehicle_type']}")
                st.write(f"**Status:** {violation['status'].upper()}")
                
                if violation['status'] == 'pending':
                    if st.button(f"PAY NOW", key=f"pay_{violation['_id']}"):
                        with st.status("Processing Payment...", expanded=True) as status:
                            st.write("Connecting to Gateway...")
                            time.sleep(1)
                            st.write("Verifying Card Details...")
                            time.sleep(1)
                            status.update(label="Payment Successful!", state="complete", expanded=False)
                        
                        st.success(f"✅ Paid LKR {violation['fine_amount']:,.0f}")
                        st.balloons()

    except Exception as e:
        st.error(f"Error: {e}")


def show_vehicles_tab():
    """Vehicles management tab"""
    st.write("")
    st.write("### MY FLEET")

    if not st.session_state.get('db_connected'):
        st.warning("System Offline")
        return

    try:
        user_vehicles = vehicle_ops.collection.find()
        vehicle_list = list(user_vehicles)

        if vehicle_list:
            for vehicle in vehicle_list:
                with st.expander(f"{vehicle['license_plate']} • {vehicle['vehicle_type'].replace('parked_', '').upper()}", expanded=True):
                    st.write(f"**Make/Model:** {vehicle.get('make', '-')} {vehicle.get('model', '-')}")
                    st.write(f"**Color:** {vehicle.get('color', '-')}")

        st.write("---")
        st.write("### ADD VEHICLE")

        with st.form("add_vehicle_form"):
            new_plate = st.text_input("License Plate")
            new_type = st.selectbox("Type", ["parked_car", "parked_tuktuk", "parked_bus", "parked_van", "parked_motorcycle"])
            
            submit = st.form_submit_button("REGISTER VEHICLE")

            if submit:
                if new_plate:
                    try:
                        vehicle_ops.register_vehicle(license_plate=new_plate.upper(), vehicle_type=new_type)
                        st.success("Vehicle Added")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

    except Exception as e:
        st.error(f"Error: {e}")


def show_profile_tab():
    """Profile tab"""
    st.write("")
    st.write("### ACCOUNT SETTINGS")

    user = st.session_state.user_data

    st.info(f"Logged in as: {user['email']}")

    st.write("### NOTIFICATIONS")
    st.checkbox("Email Alerts", value=True)
    st.checkbox("SMS Alerts", value=True)

    st.write("")
    if st.button("LOGOUT"):
        st.session_state.authenticated = False
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
