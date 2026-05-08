import json
import hashlib
import html as html_lib
import numpy as np
from groq import Groq
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import os
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Please check your .env file.")


class BankingChatbot:
    def __init__(self, data_file="data.json"):
        base = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base, data_file)

        self.client = Groq(api_key=GROQ_API_KEY)
        self._load_dataset(data_path)

        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self._index_dataset(base)

    def _load_dataset(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.dataset = json.load(f)
        self.questions = [item["question"] for item in self.dataset]

    def _index_dataset(self, base_dir):
        cache_emb  = os.path.join(base_dir, ".emb_cache.npy")
        cache_hash = os.path.join(base_dir, ".emb_cache.hash")

        current_hash = hashlib.md5(
            json.dumps(self.questions, sort_keys=True).encode()
        ).hexdigest()

        if os.path.exists(cache_emb) and os.path.exists(cache_hash):
            with open(cache_hash) as f:
                if f.read().strip() == current_hash:
                    self.question_embeddings = np.load(cache_emb)
                    return

        self.question_embeddings = self.embedder.encode(
            self.questions, show_progress_bar=False
        )
        np.save(cache_emb, self.question_embeddings)
        with open(cache_hash, "w") as f:
            f.write(current_hash)

    def retrieve_context(self, query):
        emb  = self.embedder.encode([query])
        sims = cosine_similarity(emb, self.question_embeddings)[0]
        idx  = int(np.argmax(sims))
        return self.dataset[idx] if sims[idx] > 0.4 else None

    def get_response(self, query, context_item=None):
        ctx_block = (
            f"Relevant knowledge: {context_item['answer']}"
            if context_item
            else "No exact match found — draw on general banking expertise."
        )

        prompt = f"""You are Astura, a professional yet warm banking assistant.
{ctx_block}

Customer question: {query}

Reply in this exact JSON format:
{{
  "answer": "2-3 sentence conversational but professional response",
  "suggestions": ["Follow-up question 1", "Follow-up question 2", "Follow-up question 3"]
}}"""

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
            )
            raw = completion.choices[0].message.content

            data        = json.loads(raw)
            answer      = data.get("answer", "I'm sorry, I couldn't generate a response.")
            suggestions = [s.strip() for s in data.get("suggestions", [])[:3]]
            return answer, suggestions

        except Exception as e:
            print(f"Groq API Error: {e}")
            try:
                fallback_prompt = f"Answer this banking question in 2-3 sentences: {query}"
                completion = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": fallback_prompt}],
                )
                ans = completion.choices[0].message.content.strip()
                return ans, [
                    "What documents do I need to open an account?",
                    "How do I check my account balance?",
                    "What is a Fixed Deposit?",
                ]
            except Exception:
                return (
                    "I'm having a little trouble connecting right now. Please try again in a moment.",
                    [
                        "What documents do I need to open an account?",
                        "How do I check my account balance?",
                        "What is a Fixed Deposit?",
                    ],
                )

    def chat_loop(self):
        print("\n— Astura Banking Assistant —\nType 'exit' to quit.\n")
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ("exit", "quit"):
                    print("Astura: Goodbye! Have a great day.")
                    break
                ctx    = self.retrieve_context(user_input)
                answer, _ = self.get_response(user_input, ctx)
                print(f"Astura: {answer}\n")
            except KeyboardInterrupt:
                print("\nAstura: Goodbye!")
                break


if __name__ == "__main__":
    bot = BankingChatbot()
    bot.chat_loop()
