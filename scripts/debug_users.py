
import sys
from pathlib import Path
import pprint

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from src.database import db, user_ops

def list_users():
    try:
        db.connect()
        users = user_ops.get_all_users()
        print(f"Found {len(users)} users:")
        for user in users:
            print(f"- Username: {user.get('username')}, Email: {user.get('email')}, Role: {user.get('role')}")
            # print(f"  Hashed Password: {user.get('hashed_password')}") 
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_users()
