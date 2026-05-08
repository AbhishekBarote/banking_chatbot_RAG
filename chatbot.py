import json
import numpy as np
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import warnings

# Suppress warnings for cleaner CLI output
warnings.filterwarnings("ignore")

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 1. Setup Gemini LLM using API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")

genai.configure(api_key=GEMINI_API_KEY)
llm = genai.GenerativeModel('gemini-2.5-flash')


class BankingChatbot:
    def __init__(self, data_file='data.json'):
        # Support running from any directory
        data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), data_file)
        print("Loading Banking Chatbot...")
        self.load_dataset(data_file)
        
        # 2. Setup Embeddings: Using Sentence Transformers as recommended
        print("Loading local embedding model (Sentence Transformers)...")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        print("Indexing dataset...")
        self.index_dataset()
        print("\n--- Chatbot Ready! ---")
        print("Type 'exit' or 'quit' to stop.")

    def load_dataset(self, data_file):
        """Loads the banking Q&A dataset."""
        with open(data_file, 'r', encoding='utf-8') as f:
            self.dataset = json.load(f)
        self.questions = [item['question'] for item in self.dataset]

    def index_dataset(self):
        """Converts the dataset questions into embeddings."""
        self.question_embeddings = self.embedder.encode(self.questions)

    def retrieve_context(self, query):
        """3. Simple Retrieval: Finds the most similar question from the dataset."""
        query_embedding = self.embedder.encode([query])
        similarities = cosine_similarity(query_embedding, self.question_embeddings)[0]
        best_match_index = np.argmax(similarities)
        
        # If the highest similarity is too low, we assume no relevant info found
        if similarities[best_match_index] > 0.4:
            return self.dataset[best_match_index]
        return None

    def get_answer(self, query, context_item):
        """4. LLM Response: Passes retrieved text and query to LLM."""
        if context_item:
            prompt = f"""
            You are a helpful banking chatbot. Answer the user's question using the provided context.
            Make it sound natural and conversational.
            
            Context: {context_item['answer']}
            User Question: {query}
            """
        else:
            prompt = f"""
            You are a helpful banking chatbot. The user asked a question that is not in your primary database.
            Answer the user's question using your general banking knowledge.
            
            User Question: {query}
            """
        
        try:
            response = llm.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error connecting to LLM: {str(e)}"

    def get_recommendations(self, query, answer):
        """Suggests 3 follow-up questions."""
        prompt = f"""
        User asked: {query}
        Bot answered: {answer}
        
        Suggest exactly 3 short follow-up questions a banking customer might ask next.
        Return ONLY the questions, one per line, with no bullets or numbers.
        """
        try:
            raw = llm.generate_content(prompt).text.strip()
            questions = [line.strip() for line in raw.splitlines() if line.strip()]
            # Clean up leading dash or bullet if present
            questions = [q.lstrip("•- ") for q in questions]
            return questions[:3]
        except Exception:
            return [
                "What documents do I need?",
                "How do I check my balance?",
                "What is a fixed deposit?"
            ]

    def chat_loop(self):
        """5. Interface: Simple command-line chatbot loop."""
        while True:
            try:
                user_input = input("\nUser: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ['exit', 'quit']:
                    print("Bot: Goodbye!")
                    break

                # Step 1: Retrieve relevant information
                context = self.retrieve_context(user_input)
                
                # Step 2: Generate LLM Response
                answer = self.get_answer(user_input, context)
                
                # Step 3: Print Response
                print(f"Bot: {answer}")

            except KeyboardInterrupt:
                print("\nBot: Goodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    bot = BankingChatbot()
    bot.chat_loop()
