import os
import sys

# Add the project root to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.database.connection import db

def clear_database():
    """Drops the configured database."""
    try:
        # Connect to the database to ensure client is initialized
        db.connect()
        
        if db._client:
            db_name = os.getenv("DB_NAME", "parking_violations_db")
            print(f"⚠️  About to drop database: {db_name}")
            
            # Drop the database
            db._client.drop_database(db_name)
            print(f"✅ Database '{db_name}' has been cleared successfully.")
        else:
            print("❌ Failed to connect to database.")
            
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    clear_database()
