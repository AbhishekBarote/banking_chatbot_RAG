import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyB5GjY61taNRiod7VhqVnW50oUoOZ1dwGA"
genai.configure(api_key=GEMINI_API_KEY)

print("Available Models for this API Key:")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Failed to list models. Is the API key valid? Error: {e}")
