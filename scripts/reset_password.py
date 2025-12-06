
import sys
from pathlib import Path
import bcrypt

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from src.database import db, user_ops

def reset_password(email, new_password):
    try:
        db.connect()
        user = user_ops.get_user_by_email(email)
        if not user:
            print(f"User {email} not found.")
            return

        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        db.get_db()['users'].update_one(
            {"email": email},
            {"$set": {"hashed_password": hashed_password}}
        )
        print(f"✅ Password for {email} reset successfully.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    reset_password("ranidu@gmail.com", "password123")
