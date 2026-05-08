import json
import numpy as np
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")

genai.configure(api_key=GEMINI_API_KEY)
llm = genai.GenerativeModel('gemini-2.5-flash')

def test():
    print("Testing Chatbot Retrieval and LLM...")
    
    # Load data
    with open('data.json', 'r') as f:
        dataset = json.load(f)
    questions = [item['question'] for item in dataset]

    # Load embedder
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    question_embeddings = embedder.encode(questions)

    # Test Query
    query = "What documents do I need to open a bank account?"
    print(f"Query: {query}")
    
    query_embedding = embedder.encode([query])
    
    similarities = cosine_similarity(query_embedding, question_embeddings)[0]
    best_idx = np.argmax(similarities)
    
    context = dataset[best_idx]
    print(f"Retrieved Context: {context['question']}")
    
    # Generate response
    prompt = f"System: Banking Assistant. Context: {context['answer']}. Query: {query}"
    response = llm.generate_content(prompt)
    print(f"Bot Response: {response.text.strip()}")

if __name__ == "__main__":
    try:
        test()
    except Exception as e:
        print(f"Error: {e}")
