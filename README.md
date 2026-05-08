# Basic Banking Chatbot

This is a simple AI-powered banking assistant built as part of an internship assignment.  
It uses embeddings to search through banking-related information and an LLM to generate natural, conversational answers.

The chatbot can answer common banking questions such as:
- What is KYC?
- How to open a bank account
- Required documents for verification
- Basic banking procedures and services

It combines semantic search with generative AI so responses feel more helpful and human instead of just returning fixed text.



## 🛠️ Tech Stack
- **Python**
- **Embeddings**: `sentence-transformers`
- **LLM**: `google-generativeai` (Gemini API)
- **Math/Vector ops**: `numpy`, `scikit-learn`
- **UI Framework**: `streamlit`

## 🚀 How to Run Locally

### 1. Clone the repository and navigate to the project directory:
```bash
# git clone <https://github.com/AbhishekBarote/banking_chatbot_RAG.git>
cd (your folder)
```

### 2. Install Dependencies:
```bash
pip install -r requirements.txt
```
*(Tip: If the installation times out on a slow network due to large packages, use: `pip install -r requirements.txt --default-timeout=1000`)*

### 3. Run the Streamlit UI (Recommended):
```bash
streamlit run app.py
```

### 4. Run the Command-Line Version (CLI):
```bash
python chatbot.py
```

---

## 📸 Screenshots & Sample Queries

Here are some sample interactions demonstrating the chatbot's ability to retrieve information from the dataset and generate human-like responses, as well as recommend follow-up questions.

> **Note to evaluator/user:** The images below demonstrate the working functionality of the chatbot.

### 1. Main Chat Interface
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3e33b3a3-9685-4f63-ad92-8c22d211f28f" />


### 2. Sample Query 1: "What is KYC?"
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0652b294-0e42-4765-a3bd-4fb23c6bc0fe" />


### 3. Sample Query 2: "What documents do I need to open an account?"
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/974890d0-3f5f-4859-8b4e-43e4585e5412" />
