"""Create a test JWT token for API testing"""
import os
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

# Create token for test user with ID 1
user_id = 1
token_data = {
    "sub": str(user_id),  # Subject (user_id)
    "exp": datetime.utcnow() + timedelta(hours=24),  # Expires in 24 hours
    "iat": datetime.utcnow(),  # Issued at
}

token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

print("=" * 60)
print("TEST JWT TOKEN")
print("=" * 60)
print(f"\nUser ID: {user_id}")
print(f"Expires: {token_data['exp']}")
print(f"\nToken:\n{token}")
print("\n" + "=" * 60)
print("\nUsage:")
print(f'curl -H "Authorization: Bearer {token}" \\')
print('     http://localhost:8000/api/tasks')
print("=" * 60)
