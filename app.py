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

# ─── DETECT REAL PUBLIC URL FROM REQUEST HEADERS ──────────────────────────────
# Both st.markdown() and st.components.v1.html() create srcdoc iframes whose
# window.location.origin is "null" — so ALL browser-side URL detection fails.
# The ONLY reliable source of truth is the HTTP request headers seen by Python.
def get_asset_base() -> str:
    try:
        # st.context.headers available in Streamlit 1.33+
        headers = st.context.headers
        host = headers.get("host", "")
        if host:
            # x-forwarded-proto is set by Streamlit Cloud's reverse proxy
            proto = headers.get("x-forwarded-proto", "")
            if not proto:
                # Local dev: decide from host
                proto = "http" if ("localhost" in host or "127.0.0.1" in host) else "https"
            return f"{proto}://{host}/app/static"
    except Exception:
        pass

    # Fallback 1: STREAMLIT_URL env var (set on some cloud platforms)
    env_url = os.environ.get("STREAMLIT_URL", "").rstrip("/")
    if env_url:
        return env_url + "/app/static"

    # Fallback 2: build from st.get_option (works locally, wrong on Cloud)
    try:
        host = st.get_option("browser.serverAddress") or "localhost"
        port = st.get_option("server.port") or 8501
        proto = "http" if host in ("localhost", "127.0.0.1") else "https"
        return f"{proto}://{host}:{port}/app/static"
    except Exception:
        pass

    return "http://localhost:8501/app/static"

asset_base = get_asset_base()

# ─── READ & PATCH GAME HTML ────────────────────────────────────────────────────
with open("game.html", "r", encoding="utf-8") as f:
    game_html = f.read()

# Inject the asset base as the very first script — this overwrites the JS
# fallback chain so Phaser always gets the correct URL immediately.
injection = f'<script>window.__ASSET_BASE__ = "{asset_base}";</script>'
game_html = game_html.replace("</head>", injection + "\n</head>", 1)

# ─── RENDER ───────────────────────────────────────────────────────────────────
# height=10000 prevents the wrapper div from clipping the fixed iframe on
# short mobile viewports (iPhone SE, landscape with browser chrome, etc.)
st.components.v1.html(game_html, height=10000, scrolling=False)