"""MongoDB database connection management."""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class Database:
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        """Establish MongoDB connection."""
        if self._client is None:
            mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
            db_name = os.getenv("DB_NAME", "parking_violations_db")
            
            self._client = MongoClient(mongodb_uri)
            self._db = self._client[db_name]
            print(f"✅ Connected to MongoDB: {db_name}")
        
        return self._db
    
    def get_db(self):
        """Get database instance."""
        if self._db is None:
            return self.connect()
        return self._db
    
    def close(self):
        """Close MongoDB connection."""
        if self._client:
            self._client.close()
            print("✅ MongoDB connection closed")

# Global database instance
db = Database()