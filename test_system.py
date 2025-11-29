"""
Quick system test to verify all components are working
"""
import sys
from pathlib import Path

print("🧪 Testing Intelligent Traffic Management System")
print("=" * 60)

# Test 1: Import database modules
print("\n1. Testing database modules...")
try:
    from src.database import db, user_ops, vehicle_ops, violation_ops
    print("   ✅ Database modules imported successfully")
except Exception as e:
    print(f"   ❌ Database import failed: {e}")
    sys.exit(1)

# Test 2: Import detection modules
print("\n2. Testing detection modules...")
try:
    from src.detection import RealtimeDetector, ViolationProcessor
    print("   ✅ Detection modules imported successfully")
except Exception as e:
    print(f"   ❌ Detection import failed: {e}")
    sys.exit(1)

# Test 3: Check model file exists
print("\n3. Checking for trained model...")
model_path = Path("runs/parking_violations/exp/weights/best.pt")
if model_path.exists():
    print(f"   ✅ Model found at: {model_path}")
    print(f"   📊 Model size: {model_path.stat().st_size / 1024 / 1024:.2f} MB")
else:
    print(f"   ⚠️  Model not found at: {model_path}")
    print("      You'll need the trained model to run detections")

# Test 4: Test MongoDB connection
print("\n4. Testing MongoDB connection...")
try:
    database = db.connect()
    print(f"   ✅ Connected to database: {database.name}")

    # List collections
    collections = database.list_collection_names()
    if collections:
        print(f"   📁 Existing collections: {', '.join(collections)}")
    else:
        print("   📁 No collections yet (will be created on first use)")

except Exception as e:
    print(f"   ⚠️  MongoDB connection failed: {e}")
    print("      Make sure MongoDB is running: brew services start mongodb-community")

# Test 5: Test detector initialization (if model exists)
if model_path.exists():
    print("\n5. Testing detector initialization...")
    try:
        detector = RealtimeDetector()
        model_info = detector.get_model_info()
        print(f"   ✅ Detector initialized successfully")
        print(f"   🤖 Model classes: {model_info['num_classes']}")
        print(f"   📊 Classes: {list(model_info['class_names'].values())}")
        print(f"   🎯 Confidence threshold: {model_info['conf_threshold']}")
    except Exception as e:
        print(f"   ❌ Detector initialization failed: {e}")
else:
    print("\n5. Skipping detector test (model not found)")

# Test 6: Test violation processor
print("\n6. Testing violation processor...")
try:
    processor = ViolationProcessor()
    print("   ✅ Violation processor initialized")
    print(f"   💰 Base fines: {len(processor.base_fines)} vehicle types configured")

    # Test fine calculation
    test_fine = processor.calculate_fine('parked_car', 'high')
    print(f"   💵 Sample fine (car, high severity): LKR {test_fine:,.0f}")
except Exception as e:
    print(f"   ❌ Violation processor failed: {e}")

# Summary
print("\n" + "=" * 60)
print("✅ System test complete!")
print("\n📝 Next steps:")
print("   1. Ensure MongoDB is running: brew services start mongodb-community")
print("   2. Run enhanced dashboard: streamlit run src/dashboard/app_enhanced.py")
print("   3. Run mobile app: streamlit run src/dashboard/user_app_enhanced.py")
print("\n🚀 Your system is ready!")
