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

  /* Pin the game iframe to the full viewport on ALL screen sizes.
     height=10000 on the component guarantees the wrapper div never clips it. */
  iframe {
    position: fixed !important;
    top: 0 !important; left: 0 !important;
    width: 100vw !important; height: 100vh !important;
    border: none !important;
    z-index: 9999 !important;
    /* Allow the Fullscreen API and pointer-lock inside the iframe */
    allow: fullscreen; allowfullscreen: true;
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

# ─── RENDER GAME ───────────────────────────────────────────────────────────────
with open("game.html", "r", encoding="utf-8") as f:
    game_html = f.read()

# ── INJECT ASSET BASE ─────────────────────────────────────────────────────────
try:
    streamlit_url = os.environ.get("STREAMLIT_URL", "").rstrip("/")
    if not streamlit_url:
        host = st.get_option("browser.serverAddress") or "localhost"
        port = st.get_option("server.port") or 8501
        scheme = "https" if host not in ("localhost", "127.0.0.1") else "http"
        streamlit_url = f"{scheme}://{host}:{port}"

    asset_base = streamlit_url + "/app/static"
    injection = f'<script>window.__ASSET_BASE__="{asset_base}";</script>'
    game_html = game_html.replace("</head>", injection + "\n</head>", 1)
except Exception:
    pass

# ─── RENDER ───────────────────────────────────────────────────────────────────
# height=10000 makes the wrapper div taller than any real screen so the CSS
# `height:100vh` on the iframe is never clipped — critical on short mobile
# viewports (e.g. iPhone SE, landscape phones with browser chrome visible).
st.components.v1.html(game_html, height=10000, scrolling=False)