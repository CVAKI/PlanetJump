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
    position: fixed !important;
    top: 0 !important; left: 0 !important;
    width: 100vw !important; height: 100vh !important;
    border: none !important;
    z-index: 9999 !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── PARENT-PAGE ASSET BRIDGE ──────────────────────────────────────────────────
# The game iframe has origin=null (srcdoc), so it cannot read window.location
# itself. This script lives in the PARENT Streamlit page where window.location
# IS the real public URL. It listens for the iframe's REQUEST_ASSET_BASE
# message and replies with the correct origin — works on localhost, Streamlit
# Cloud, and all mobile browsers without any server-side URL guessing.
st.markdown("""
<script>
(function() {
  var assetBase = window.location.origin + '/app/static';

  function sendToAllIframes() {
    document.querySelectorAll('iframe').forEach(function(f) {
      try {
        f.contentWindow.postMessage(
          { type: 'STREAMLIT_ASSET_BASE', url: assetBase }, '*'
        );
      } catch(e) {}
    });
  }

  // Reply whenever the iframe asks
  window.addEventListener('message', function(e) {
    if (e.data && e.data.type === 'REQUEST_ASSET_BASE') {
      sendToAllIframes();
    }
  });

  // Also push proactively in case the request fires before listener is ready
  setTimeout(sendToAllIframes, 800);
  setTimeout(sendToAllIframes, 2500);
})();
</script>
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

# ── Server-side injection (kept as a fallback; postMessage above is primary) ──
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

# height=10000 ensures the fixed-position iframe is never clipped on short
# mobile viewports (iPhone SE, landscape phones with browser chrome, etc.)
st.components.v1.html(game_html, height=10000, scrolling=False)