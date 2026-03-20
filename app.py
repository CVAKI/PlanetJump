import streamlit as st
import os
import socket

st.set_page_config(
    page_title="🪐 Planet Jumpers: Coin Rush",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  #MainMenu, header, footer, .stDeployButton,
  section[data-testid="stSidebar"] { display: none !important; }
  .block-container { padding: 0 !important; margin: 0 !important;
                     max-width: 100% !important; }
  .stApp { background: #1a1a2e; overflow: hidden; }
  iframe { position: fixed !important; top: 0 !important; left: 0 !important;
           width: 100vw !important; height: 100vh !important;
           border: none !important; z-index: 9999 !important; }
</style>
""", unsafe_allow_html=True)

if not os.path.exists("game.html"):
    st.error("⚠️  game.html not found"); st.stop()
if not os.path.exists("static/assets/Sprites/Characters/character_pink_idle.png"):
    st.error("⚠️  Assets missing"); st.stop()

with open("game.html", "r", encoding="utf-8") as f:
    game_html = f.read()

def get_streamlit_url():
    # 1. Streamlit Cloud sets this env var automatically
    url = os.environ.get("STREAMLIT_URL", "").rstrip("/")
    if url:
        return url
    # 2. Configured host (cloud deployments / custom domain)
    try:
        host = st.get_option("browser.serverAddress") or ""
        port = st.get_option("server.port") or 8501
        if host and host not in ("localhost", "127.0.0.1", "0.0.0.0"):
            scheme = "https" if not host.replace(".","").isdigit() else "http"
            return f"{scheme}://{host}:{port}"
    except Exception:
        pass
    # 3. LAN IP — critical for Android on same WiFi as the dev machine
    try:
        port = st.get_option("server.port") or 8501
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        lan_ip = s.getsockname()[0]
        s.close()
        return f"http://{lan_ip}:{port}"
    except Exception:
        pass
    return "http://localhost:8501"

try:
    streamlit_url = get_streamlit_url()
    asset_base    = streamlit_url + "/app/static"
    injection     = f'<script>window.__ASSET_BASE__="{asset_base}";</script>'
    game_html     = game_html.replace("</head>", injection + "\n</head>", 1)
except Exception:
    pass

st.components.v1.html(game_html, height=750, scrolling=False)