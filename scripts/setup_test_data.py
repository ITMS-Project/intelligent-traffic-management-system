#!/usr/bin/env python3
"""
Setup Test Data for Real-time Detection
Adds sample drivers and vehicles to test the complete flow
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.database.connection import Database
from bson import ObjectId
import bcrypt
from datetime import datetime


def setup_test_data():
    """Add test drivers and vehicles to database."""
    print("🔧 Setting up test data for real-time detection...\n")

    db_instance = Database()
    db = db_instance.get_db()
    users_col = db['users']
    vehicles_col = db['vehicles']

    # Test drivers with various license plates
    test_users = [
        {
            'username': 'nimal_silva',
            'email': 'nimal@example.com',
            'password': 'test123',
            'full_name': 'Nimal Silva',
            'phone': '+94771234567',
            'vehicles': [
                {'plate': 'WP CAB-1234', 'type': 'car', 'make': 'Toyota', 'model': 'Axio', 'color': 'White'},
                {'plate': 'WP-5678', 'type': 'car', 'make': 'Honda', 'model': 'Civic', 'color': 'Black'},
            ]
        },
        {
            'username': 'kamala_perera',
            'email': 'kamala@example.com',
            'password': 'test123',
            'full_name': 'Kamala Perera',
            'phone': '+94712345678',
            'vehicles': [
                {'plate': 'CP-1111', 'type': 'van', 'make': 'Nissan', 'model': 'Caravan', 'color': 'Silver'},
            ]
        },
        {
            'username': 'tharindu_fernando',
            'email': 'tharindu@example.com',
            'password': 'test123',
            'full_name': 'Tharindu Fernando',
            'phone': '+94723456789',
            'vehicles': [
                {'plate': 'SP LD-2222', 'type': 'tuktuk', 'make': 'Bajaj', 'model': 'RE', 'color': 'Yellow'},
                {'plate': 'SP-3333', 'type': 'motorcycle', 'make': 'Honda', 'model': 'CD 70', 'color': 'Red'},
            ]
        },
        {
            'username': 'admin_user',
            'email': 'admin@example.com',
            'password': 'admin123',
            'full_name': 'System Admin',
            'phone': '+94701234567',
            'role': 'admin',
            'vehicles': []
        }
    ]

    created_count = 0

    for user_data in test_users:
        # Check if user already exists
        existing = users_col.find_one({'username': user_data['username']})
        if existing:
            print(f"⚠️  User '{user_data['username']}' already exists, skipping...")
            continue

        # Create user
        vehicles = user_data.pop('vehicles')
        password = user_data.pop('password')

        user_doc = {
            'username': user_data['username'],
            'email': user_data['email'],
            'password_hash': bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
            'role': user_data.get('role', 'driver'),
            'full_name': user_data['full_name'],
            'phone': user_data['phone'],
            'safety_score': 100,
            'score_badge': 'Excellent',
            'created_at': datetime.utcnow(),
            'fcm_token': f'demo-token-{user_data["username"]}'  # For notifications
        }

        user_result = users_col.insert_one(user_doc)
        user_id = user_result.inserted_id
        print(f"✅ Created user: {user_data['username']} (ID: {user_id})")

        # Add vehicles for this user
        for vehicle_data in vehicles:
            # Check if vehicle exists
            existing_vehicle = vehicles_col.find_one({'license_plate': vehicle_data['plate']})
            if existing_vehicle:
                print(f"   ⚠️  Vehicle {vehicle_data['plate']} already exists, skipping...")
                continue

            vehicle_doc = {
                'owner_id': str(user_id),
                'license_plate': vehicle_data['plate'],
                'vehicle_type': vehicle_data['type'],
                'make': vehicle_data['make'],
                'model': vehicle_data['model'],
                'color': vehicle_data['color'],
                'year': 2020,
                'registered_at': datetime.utcnow()
            }

            vehicle_result = vehicles_col.insert_one(vehicle_doc)
            print(f"   🚗 Added vehicle: {vehicle_data['plate']} ({vehicle_data['type']})")

        created_count += 1
        print()

    print("="*70)
    print(f"✅ Setup complete! Created {created_count} test users with vehicles")
    print("="*70)
    print()
    print("📋 Test License Plates:")
    print("   • WP CAB-1234 (Nimal's car)")
    print("   • WP-5678 (Nimal's second car)")
    print("   • CP-1111 (Kamala's van)")
    print("   • SP LD-2222 (Tharindu's tuktuk)")
    print("   • SP-3333 (Tharindu's motorcycle)")
    print()
    print("🔐 Test Credentials:")
    print("   Username: nimal_silva")
    print("   Password: test123")
    print()
    print("   Username: kamala_perera")
    print("   Password: test123")
    print()
    print("   Username: tharindu_fernando")
    print("   Password: test123")
    print()
    print("   Username: admin_user (Authority)")
    print("   Password: admin123")
    print()
    print("🎯 Next Steps:")
    print("   1. Run real-time detection:")
    print("      python run_realtime_detection.py --mode webcam")
    print()
    print("   2. Or test with video:")
    print("      python run_realtime_detection.py --mode video --video your_video.mp4")
    print()
    print("   3. View violations in mobile app:")
    print("      streamlit run src/dashboard/driver_mobile_app.py --server.port 8502")
    print()


if __name__ == "__main__":
    try:
        setup_test_data()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
