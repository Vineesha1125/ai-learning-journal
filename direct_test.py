import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')

print("=== Testing Gemini API ===")
print(f"Using API Key: {API_KEY[:15]}...")

try:
    genai.configure(api_key=API_KEY)
    print("✅ API configured successfully\n")
    
    # List all available models
    print("=== Available Models ===")
    models_found = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ {m.name}")
            models_found.append(m.name)
    
    if not models_found:
        print("❌ No models found that support generateContent")
    
    # Try generating content with different model names
    print("\n=== Testing Content Generation ===")
    
    test_models = [
        'gemini-1.5-flash',
        'gemini-pro',
        'models/gemini-1.5-flash',
        'models/gemini-pro'
    ]
    
    for model_name in test_models:
        try:
            print(f"\nTrying model: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say hello!")
            print(f"✅ SUCCESS with {model_name}")
            print(f"Response: {response.text}")
            break
        except Exception as e:
            print(f"❌ Failed with {model_name}: {str(e)[:100]}")
    
except Exception as e:
    print(f"\n❌ Main Error: {e}")
    import traceback
    traceback.print_exc()