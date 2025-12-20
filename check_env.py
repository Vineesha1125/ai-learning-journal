from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')

print("=== Environment Check ===")
print(f"API Key exists: {api_key is not None}")
if api_key:
    print(f"API Key starts with: {api_key[:10]}...")
    print(f"API Key length: {len(api_key)}")
else:
    print("❌ API Key not found!")
    print("\nChecking .env file location...")
    print(f"Current directory: {os.getcwd()}")
    print(f".env file exists: {os.path.exists('.env')}")