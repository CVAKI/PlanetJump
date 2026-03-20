import streamlit as st
import os

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🪐 Planet Jumpers: Coin Rush",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── HIDE ALL STREAMLIT CHROME ─────────────────────────────────────────────────
st.markdown("""
<style>
  #MainMenu, header, footer, .stDeployButton,
  section[data-testid="stSidebar"] { display: none !important; }
  .block-container { padding: 0 !important; margin: 0 !important;
                     max-width: 100% !important; }
  .stApp { background: #1a1a2e; overflow: hidden; }
  iframe {
    position: fixed !important; top: 0 !important; left: 0 !important;
    width: 100vw !important; height: 100vh !important;
    border: none !important; z-index: 9999 !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── VERIFY FILES ──────────────────────────────────────────────────────────────
if not os.path.exists("game.html"):
    st.error("⚠️  game.html not found — place it next to app.py")
    st.stop()

if not os.path.exists("static/assets/Sprites/Characters/character_pink_idle.png"):
    st.error("⚠️  Assets missing. Make sure static/assets/ contains the Kenney sprites.")
    st.stop()

# ─── READ GAME HTML ────────────────────────────────────────────────────────────
with open("game.html", "r", encoding="utf-8") as f:
    game_html = f.read()

# ─── NO SERVER-SIDE URL INJECTION ─────────────────────────────────────────────
# st.context.headers captures internal WebSocket headers, NOT the browser's
# real request — so on Streamlit Cloud it always shows "localhost:8501" which
# is wrong. Injecting that URL breaks asset loading on mobile.
#
# Instead, game.html detects the correct URL entirely in the browser using:
#   1. window.location.ancestorOrigins  (Chrome / Android Chrome — most reliable)
#   2. document.referrer                (Firefox fallback)
# Both work correctly inside Streamlit's srcdoc iframes on the real public URL.

# ─── RENDER ────────────────────────────────────────────────────────────────────
st.components.v1.html(game_html, height=10000, scrolling=False)