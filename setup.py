import streamlit as st
import os

st.set_page_config(
    page_title="🗺️ Planet Jumpers — Level Editor",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  #MainMenu, header, footer, .stDeployButton,
  section[data-testid="stSidebar"] { display: none !important; }
  .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
  .stApp { background: #12121f; overflow: hidden; }
  iframe { position: fixed !important; top: 0 !important; left: 0 !important;
           width: 100vw !important; height: 100vh !important;
           border: none !important; z-index: 9999 !important; }
</style>
""", unsafe_allow_html=True)

if not os.path.exists("editor.html"):
    st.error("⚠️  editor.html not found — place it next to setup.py")
    st.stop()

if not os.path.exists("static/assets/Sprites/Tiles/terrain_grass_block_top.png"):
    st.error("⚠️  Assets missing. Ensure static/assets/ contains the Kenney sprites.")
    st.stop()

with open("editor.html", "r", encoding="utf-8") as f:
    editor_html = f.read()

# ── INJECT ASSET BASE ─────────────────────────────────────────────────────────
# Detect the Streamlit server origin so the iframe can resolve asset URLs
# correctly even when ancestorOrigins / referrer detection fails in the browser.
#
# Priority order:
#   1. STREAMLIT_URL env var  (set on Streamlit Cloud automatically)
#   2. st.get_option browser.serverAddress + port  (works locally)
#   3. No injection — JS in-browser detection takes over
try:
    streamlit_url = os.environ.get("STREAMLIT_URL", "").rstrip("/")
    if not streamlit_url:
        host = st.get_option("browser.serverAddress") or "localhost"
        port = st.get_option("server.port") or 8501
        scheme = "https" if host not in ("localhost", "127.0.0.1") else "http"
        streamlit_url = f"{scheme}://{host}:{port}"

    asset_base = streamlit_url + "/app/static"
    injection = f'<script>window.__ASSET_BASE__="{asset_base}";</script>'
    # Insert just before the closing </head>
    editor_html = editor_html.replace("</head>", injection + "\n</head>", 1)
except Exception:
    pass  # JS in-browser detection will handle it

# ─────────────────────────────────────────────────────────────────────────────
st.components.v1.html(editor_html, height=750, scrolling=False)