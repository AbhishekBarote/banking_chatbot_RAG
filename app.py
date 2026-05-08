"""
Atura Banking Assistant — Streamlit UI
Run with:  streamlit run app.py
"""

import streamlit as st
from chatbot import BankingChatbot

# ── Page Config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="Astura Banking Assistant",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Google Font ---- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ---- App background ---- */
.stApp {
    background: linear-gradient(160deg, #0f172a 0%, #1e3a8a 50%, #0f172a 100%);
    min-height: 100vh;
}

/* ---- Header card ---- */
.header-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 28px 32px 20px;
    text-align: center;
    backdrop-filter: blur(12px);
    margin-bottom: 28px;
}
.header-card h1 {
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 6px;
    letter-spacing: -0.5px;
}
.header-card p {
    color: #93c5fd;
    font-size: 0.95rem;
    margin: 0;
}

/* ---- Chat message overrides ---- */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(8px);
    padding: 14px 18px !important;
    margin-bottom: 10px !important;
    color: #f1f5f9 !important;
}

/* ---- Chat input ---- */
[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 12px !important;
    color: #f1f5f9 !important;
    font-family: 'Inter', sans-serif;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #94a3b8 !important;
}

/* ---- Follow-up suggestion chips ---- */
.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 6px;
}
.chip-label {
    font-size: 0.72rem;
    font-weight: 500;
    color: #93c5fd;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
    margin-top: 16px;
}

/* Style Streamlit buttons as chips */
.stButton > button {
    background: rgba(59,130,246,0.15) !important;
    color: #bfdbfe !important;
    border: 1px solid rgba(96,165,250,0.35) !important;
    border-radius: 999px !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    padding: 8px 16px !important;
    transition: all 0.2s ease !important;
    white-space: normal !important;
    text-align: left !important;
}
.stButton > button:hover {
    background: rgba(59,130,246,0.35) !important;
    border-color: #60a5fa !important;
    color: #ffffff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(59,130,246,0.25) !important;
}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: rgba(15,23,42,0.85) !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* ---- Divider ---- */
hr {
    border-color: rgba(255,255,255,0.08) !important;
    margin: 12px 0 !important;
}

/* ---- Spinner ---- */
.stSpinner > div {
    border-top-color: #60a5fa !important;
}
</style>
""", unsafe_allow_html=True)


# ── Load chatbot (cached — runs only once per session) ──────────────────────
@st.cache_resource(show_spinner="Loading AI model...")
def load_chatbot() -> BankingChatbot:
    return BankingChatbot()

bot = load_chatbot()

# ── Session state ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []          # list of {"role": str, "content": str}
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []      # list of str

# ── Callback for chip clicks (runs before script execution) ─────────────────
def handle_chip_click(query: str):
    process_query(query)

def process_query(query: str):
    """Run retrieval + LLM and append results to session state immediately."""
    st.session_state.messages.append({"role": "user", "content": query})
    context = bot.retrieve_context(query)
    answer = bot.get_answer(query, context)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.suggestions = bot.get_recommendations(query, answer)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-card">
    <h1>🏦 Astura Banking Assistant</h1>
    <p>Ask me anything about banking — KYC, accounts, cards, and more.</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏦 About Astura")
    st.markdown("""
**Astura** is an AI-powered banking assistant that combines:
- ⚡ **Sentence Transformers** for instant local retrieval
- 🤖 **Gemini 2.5** for human-like responses
- 💬 **Context-aware recommendations**
    """)
    st.divider()
    st.markdown("**Try asking:**")
    starter_qs = [
        "What is KYC?",
        "What is a savings account?",
        "How do I open a bank account?",
        "What is a Fixed Deposit?",
        "What is a credit card?",
    ]
    for q in starter_qs:
        st.button(q, key=f"starter_{q}", on_click=handle_chip_click, args=(q,), use_container_width=True)

    st.divider()
    def clear_chat():
        st.session_state.messages = []
        st.session_state.suggestions = []
    st.button("🗑️ Clear Conversation", on_click=clear_chat, use_container_width=True)

# ── Welcome message on first load ─────────────────────────────────────────────
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(
            "👋 Hello! I'm your **Astura Banking Assistant**. "
            "Ask me about KYC, savings accounts, required documents, credit cards, and more!"
        )

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Follow-up suggestion chips ────────────────────────────────────────────────
if st.session_state.suggestions:
    st.markdown('<p class="chip-label">💡 Suggested follow-ups</p>', unsafe_allow_html=True)
    for i, suggestion in enumerate(st.session_state.suggestions):
        st.button(suggestion, key=f"chip_{i}_{suggestion[:15]}", on_click=handle_chip_click, args=(suggestion,), use_container_width=True)

# ── Chat input ────────────────────────────────────────────────────────────────
if user_input := st.chat_input("Ask a banking question..."):
    # Display user input instantly
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Process and display assistant response smoothly
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            context = bot.retrieve_context(user_input)
            answer = bot.get_answer(user_input, context)
            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    
    # Generate and save recommendations for the next script run
    st.session_state.suggestions = bot.get_recommendations(user_input, answer)
    st.rerun()
