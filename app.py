import html as html_lib
import base64
import os
import streamlit as st
from datetime import datetime
from chatbot import BankingChatbot

st.set_page_config(
    page_title="Banking Chatbot",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

def _img_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

_hero_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets", "hero.png"
)
_hero_b64 = _img_b64(_hero_path)
_hero_src  = f"data:image/png;base64,{_hero_b64}" if _hero_b64 else ""

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"/>
<style>
.material-symbols-outlined {
    font-variation-settings:'FILL' 0,'wght' 400,'GRAD' 0,'opsz' 24;
    font-family:'Material Symbols Outlined';
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
:root{
  --primary:#795916;--primary-container:#b8924a;--on-primary-container:#412c00;
  --bg:#fff8f3;--surface:#fff8f3;--surface-low:#fbf2e9;--surface-c:#f5ece3;
  --surface-high:#efe7de;--surface-highest:#eae1d8;--surface-lowest:#ffffff;
  --on-surface:#1f1b16;--on-variant:#4e4638;--outline:#807667;
  --outline-variant:#d1c5b3;--sec-container:#e5dfd5;--sec-fixed:#e8e2d8;
  --sage:#E4EFE6;--on-sec-container:#66625a;
}
*,*::before,*::after{box-sizing:border-box}
html,body,.stApp{background:var(--bg)!important;font-family:'Inter',system-ui,sans-serif;color:var(--on-surface)}
#MainMenu,footer,header{visibility:hidden}
.block-container{padding:0!important;max-width:100%!important}

/* scrollbar */
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-thumb{background:var(--outline-variant);border-radius:4px}

/* ── sidebar ── */
[data-testid="stSidebar"]{background:var(--surface-low)!important;border-right:1px solid var(--outline-variant)!important}
[data-testid="stSidebar"]>div{padding:0!important}
[data-testid="stSidebar"] hr{border-color:var(--outline-variant)!important;margin:.25rem 1.5rem!important}
[data-testid="stSidebar"] .stButton>button{
  background:transparent!important;color:var(--on-variant)!important;
  border:1px solid var(--outline-variant)!important;border-radius:12px!important;
  font-size:.78rem!important;padding:8px 16px!important;
  width:calc(100% - 3rem)!important;margin:0 1.5rem!important;
  font-family:'Inter',sans-serif!important;box-shadow:none!important;
}
[data-testid="stSidebar"] .stButton>button:hover{background:var(--sec-fixed)!important;color:var(--on-surface)!important}

/* ── nav ── */
.astura-nav{display:flex;flex-direction:column;padding:2rem 0 1rem}
.nav-brand{padding:0 1.5rem 1.5rem;border-bottom:1px solid var(--outline-variant);margin-bottom:1rem}
.nav-brand-title{display:block;font-family:'Playfair Display',serif;font-size:1.15rem;font-weight:700;color:var(--primary);line-height:1.3}
.nav-brand-sub{display:block;font-size:.68rem;color:var(--on-variant);font-weight:500;letter-spacing:.02em;margin-top:3px}
.nav-items{display:flex;flex-direction:column;gap:3px;padding:0 .75rem}
.nav-item{display:flex;align-items:center;gap:12px;padding:10px 14px;border-radius:10px;text-decoration:none;color:var(--on-variant);font-size:.82rem;font-weight:500;transition:background .14s}
.nav-item:hover{background:var(--sec-fixed);color:var(--on-surface)}
.nav-item.active{background:var(--sec-container);color:var(--on-surface);font-weight:600}
.nav-item .material-symbols-outlined{font-size:20px}
.nav-user{display:flex;align-items:center;gap:10px;padding:1rem 1.5rem;border-top:1px solid var(--outline-variant);margin-top:1rem}
.nav-user-avatar{width:36px;height:36px;border-radius:50%;background:var(--primary-container);color:var(--on-primary-container);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;flex-shrink:0}
.nav-user-name{font-size:.82rem;font-weight:700;color:var(--on-surface)}
.nav-user-ver{font-size:.63rem;color:var(--on-variant)}

/* ── top header ── */
.astura-header{display:flex;justify-content:space-between;align-items:center;background:var(--surface);padding:0 2rem;height:64px;border-bottom:1px solid var(--outline-variant);position:sticky;top:0;z-index:40}
.header-brand{display:flex;align-items:center;gap:12px}
.header-avatar{width:32px;height:32px;border-radius:50%;background:var(--primary-container);color:var(--on-primary-container);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px}
.header-title{font-family:'Playfair Display',serif;font-size:1.35rem;font-weight:700;color:var(--primary);margin:0}
.header-status{display:flex;align-items:center;gap:7px;font-size:.75rem;font-weight:600;color:var(--primary);letter-spacing:.02em}
.header-status-dot{width:8px;height:8px;border-radius:50%;background:#3A9A5A;animation:pulse-dot 2.5s ease-in-out infinite}
@keyframes pulse-dot{0%,100%{opacity:1}50%{opacity:.35}}

/* ── chat canvas ── */
.chat-canvas{padding:2rem 2.5rem;max-width:900px;margin:0 auto;display:flex;flex-direction:column;gap:2rem}

/* welcome card */
.welcome-card{background:#fff;border:1px solid var(--outline-variant);border-radius:16px;padding:2rem;display:flex;align-items:center;gap:2rem;box-shadow:0 1px 4px rgba(0,0,0,.05)}
.welcome-card-body h2{font-family:'Playfair Display',serif;font-size:1.25rem;font-weight:700;color:var(--primary);margin:0 0 .5rem}
.welcome-card-body p{font-size:.88rem;color:var(--on-variant);line-height:1.6;margin:0}
.welcome-card-img{width:90px;height:90px;border-radius:50%;overflow:hidden;flex-shrink:0;background:var(--surface-c);display:flex;align-items:center;justify-content:center}
.welcome-card-img img{width:100%;height:100%;object-fit:cover;filter:grayscale(.1) brightness(1.05)}
.welcome-card-placeholder{width:90px;height:90px;border-radius:50%;background:linear-gradient(135deg,#ebc073 0%,#b8924a 100%);display:flex;align-items:center;justify-content:center;flex-shrink:0;font-family:'Playfair Display',serif;font-size:2rem;color:#fff;font-weight:700}

/* chat messages */
.chat-history{display:flex;flex-direction:column;gap:1.5rem}

/* user bubble */
.msg-user{display:flex;flex-direction:column;align-items:flex-end;max-width:85%;margin-left:auto;animation:msg-in .2s ease}
.msg-user-bubble{background:var(--primary-container);color:var(--on-primary-container);padding:14px 20px;border-radius:18px 18px 4px 18px;font-size:.9rem;line-height:1.55}
.msg-time{font-size:.65rem;color:var(--on-variant);margin-top:4px;font-weight:500}

/* bot bubble */
.msg-bot{display:flex;gap:12px;max-width:90%;animation:msg-in .2s ease}
.msg-bot-avatar{width:40px;height:40px;border-radius:50%;background:var(--surface-high);border:1px solid var(--outline-variant);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.msg-bot-avatar .material-symbols-outlined{font-size:20px;color:var(--primary)}
.msg-bot-inner{display:flex;flex-direction:column;gap:5px}
.msg-bot-bubble{background:#fff;border:1px solid var(--outline-variant);padding:16px 20px;border-radius:18px 18px 18px 4px;box-shadow:0 2px 8px rgba(28,26,20,.04)}
.msg-bot-label{font-size:.72rem;font-weight:700;color:var(--primary);letter-spacing:.03em;margin-bottom:6px}
.msg-bot-text{font-size:.88rem;line-height:1.65;color:var(--on-surface)}
.msg-bot-text strong{color:var(--primary)}

@keyframes msg-in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}

/* thinking */
.msg-thinking{display:flex;gap:12px;align-items:flex-end}
.thinking-bubble{background:#fff;border:1px solid var(--outline-variant);padding:14px 18px;border-radius:18px 18px 18px 4px;display:flex;gap:5px;align-items:center;box-shadow:0 2px 8px rgba(28,26,20,.04)}
.td{width:5px;height:5px;background:var(--outline);border-radius:50%}
.td:nth-child(1){animation:tdot 1.2s 0s ease-in-out infinite}
.td:nth-child(2){animation:tdot 1.2s .2s ease-in-out infinite}
.td:nth-child(3){animation:tdot 1.2s .4s ease-in-out infinite}
@keyframes tdot{0%,80%,100%{transform:translateY(0);opacity:.4}40%{transform:translateY(-5px);opacity:1}}

/* suggestions */
.suggestions-bar{display:flex;flex-wrap:wrap;align-items:center;gap:.5rem;margin-bottom:.5rem}
.suggestions-label{font-size:.7rem;font-weight:600;color:var(--on-variant);letter-spacing:.04em;text-transform:uppercase;margin-right:.25rem}
.stButton>button{background:var(--surface-low)!important;border:1px solid var(--outline-variant)!important;padding:8px 16px!important;border-radius:999px!important;font-size:.8rem!important;color:var(--on-variant)!important;font-weight:500!important;cursor:pointer;transition:background .14s,border-color .14s,color .14s!important;font-family:'Inter',sans-serif!important;box-shadow:none!important}
.stButton>button:hover{background:var(--sec-fixed)!important;border-color:var(--primary)!important;color:var(--primary)!important}

/* chat input override */
[data-testid="stChatInput"]{background:var(--surface-lowest)!important;border-top:1px solid var(--outline-variant)!important;padding:1rem 2.5rem 1.5rem!important}
[data-testid="stChatInput"] textarea{background:#fff!important;border:1px solid var(--outline-variant)!important;border-radius:14px!important;color:var(--on-surface)!important;font-family:'Inter',sans-serif!important;font-size:.9rem!important;padding:14px 20px!important}
[data-testid="stChatInput"] textarea:focus{border-color:var(--primary)!important;box-shadow:0 0 0 2px rgba(121,89,22,.12)!important}
[data-testid="stChatInput"] textarea::placeholder{color:var(--outline)!important}
[data-testid="stChatInputSubmitButton"] button{background:var(--primary)!important;border-radius:12px!important;width:52px!important;height:52px!important}
[data-testid="stChatInputSubmitButton"] button:hover{background:var(--primary-container)!important}

.footer-note{text-align:center;font-size:.65rem;color:var(--on-variant);letter-spacing:.08em;text-transform:uppercase;padding:.5rem 0 0;opacity:.7}
</style>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def load_chatbot():
    return BankingChatbot()

with st.spinner(""):
    bot = load_chatbot()

if "messages"    not in st.session_state: st.session_state.messages    = []
if "suggestions" not in st.session_state: st.session_state.suggestions = []

with st.sidebar:
    st.markdown("""
    <div class="astura-nav">
      <div class="nav-brand">
        <span class="nav-brand-title">Astura Assistant</span>
        <span class="nav-brand-sub">Private Wealth Management</span>
      </div>
      <div class="nav-items">
        <a class="nav-item" href="#">
          <span class="material-symbols-outlined">verified_user</span>KYC Verification
        </a>
        <a class="nav-item active" href="#">
          <span class="material-symbols-outlined">history</span>Session History
        </a>
        <a class="nav-item" href="#">
          <span class="material-symbols-outlined">account_balance</span>Accounts &amp; Assets
        </a>
        <a class="nav-item" href="#">
          <span class="material-symbols-outlined">description</span>Secure Documents
        </a>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    n = len(st.session_state.messages) // 2
    st.markdown(f'<p style="font-size:.72rem;color:var(--on-variant);padding:0 1.5rem .5rem;margin:0">{n} exchange{"s" if n != 1 else ""} this session</p>', unsafe_allow_html=True)
    if st.button("🗑️ Clear conversation", key="clear"):
        st.session_state.messages    = []
        st.session_state.suggestions = []
        st.rerun()

    st.markdown("""
    <div class="nav-user">
      <div class="nav-user-avatar">A</div>
      <div>
        <div class="nav-user-name">Astura Client</div>
        <div class="nav-user-ver">v2.4.0</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="astura-header">
  <div class="header-brand">
    <div class="header-avatar">A</div>
    <h1 class="header-title">AI Assistant</h1>
  </div>
  <div class="header-status">
    <div class="header-status-dot"></div>Online
  </div>
</div>
""", unsafe_allow_html=True)

def _bot_html(content: str, time_str: str) -> str:
    safe = html_lib.escape(content).replace("\n", "<br>")
    import re
    safe = re.sub(r"\*\*(.+?)\*\*", r'<strong>\1</strong>', safe)
    return f"""
    <div class="msg-bot">
      <div class="msg-bot-avatar"><span class="material-symbols-outlined">account_balance_wallet</span></div>
      <div class="msg-bot-inner">
        <div class="msg-bot-bubble">
          <div class="msg-bot-label">AI Assistant</div>
          <div class="msg-bot-text">{safe}</div>
        </div>
        <span class="msg-time">{time_str}</span>
      </div>
    </div>"""

def _user_html(content: str, time_str: str) -> str:
    safe = html_lib.escape(content).replace("\n", "<br>")
    return f"""
    <div class="msg-user">
      <div class="msg-user-bubble">{safe}</div>
      <span class="msg-time">{time_str}</span>
    </div>"""

if not st.session_state.messages:
    img_html = (
        f'<div class="welcome-card-img"><img src="{_hero_src}" alt="Banking Chatbot"/></div>'
        if _hero_src
        else '<div class="welcome-card-placeholder">A</div>'
    )
    st.markdown(f"""
    <div class="chat-canvas">
      <div class="welcome-card">
        <div class="welcome-card-body">
          <h2>Good to have you here</h2>
          <p>Your private concierge for digital wealth management and asset verification.
             How may I assist your portfolio today?</p>
        </div>
        {img_html}
      </div>
    </div>
    """, unsafe_allow_html=True)
else:
    rows = [
        _bot_html(m["content"], m.get("time", "")) if m["role"] == "assistant"
        else _user_html(m["content"], m.get("time", ""))
        for m in st.session_state.messages
    ]
    st.markdown(f'<div class="chat-canvas"><div class="chat-history">{"".join(rows)}</div></div>',
                unsafe_allow_html=True)

def _fire(q: str):
    t = datetime.now().strftime("%I:%M %p")
    ctx    = bot.retrieve_context(q)
    ans, s = bot.get_response(q, ctx)
    st.session_state.messages.append({"role": "user",      "content": q,   "time": t})
    st.session_state.messages.append({"role": "assistant", "content": ans, "time": t})
    st.session_state.suggestions = s

if st.session_state.suggestions:
    st.markdown("""
    <div style="padding:.75rem 2.5rem .25rem;max-width:900px;margin:0 auto">
      <span class="suggestions-label">You might also ask:</span>
    </div>""", unsafe_allow_html=True)
    cols = st.columns(len(st.session_state.suggestions))
    for col, sug in zip(cols, st.session_state.suggestions):
        with col:
            if st.button(sug, key=f"chip_{sug[:14]}"):
                _fire(sug)
                st.rerun()

if not st.session_state.messages:
    quick = ["What is KYC?", "Open a savings account", "What is a Fixed Deposit?",
             "How to check my balance?", "Credit card basics"]
    st.markdown("""<div style="padding:.5rem 2.5rem 0;max-width:900px;margin:0 auto">
      <span class="suggestions-label">Quick topics:</span></div>""", unsafe_allow_html=True)
    cols = st.columns(len(quick))
    for col, q in zip(cols, quick):
        with col:
            if st.button(q, key=f"qt_{q[:12]}"):
                _fire(q)
                st.rerun()

st.markdown('<p class="footer-note">Encrypted end-to-end · Astura Security Standard</p>',
            unsafe_allow_html=True)

if user_input := st.chat_input("Inquire about your portfolio or security…"):
    t = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({"role": "user", "content": user_input, "time": t})
    st.session_state.suggestions = []

    ph = st.empty()
    ph.markdown("""
    <div class="chat-canvas">
      <div class="msg-thinking">
        <div class="msg-bot-avatar"><span class="material-symbols-outlined">account_balance_wallet</span></div>
        <div class="thinking-bubble"><div class="td"></div><div class="td"></div><div class="td"></div></div>
      </div>
    </div>""", unsafe_allow_html=True)

    ctx    = bot.retrieve_context(user_input)
    ans, s = bot.get_response(user_input, ctx)
    ph.empty()

    st.session_state.messages.append({"role": "assistant", "content": ans,
                                      "time": datetime.now().strftime("%I:%M %p")})
    st.session_state.suggestions = s
    st.rerun()
