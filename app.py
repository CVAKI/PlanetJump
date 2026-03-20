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

# ─── INJECT ASSET BASE DIRECTLY FROM BROWSER ──────────────────────────────────
# st.markdown() strips <script> tags so we CANNOT use it for JS.
# Instead we embed a tiny hidden st.components.v1.html() snippet whose ONLY job
# is to run in the Streamlit parent page (where window.location is the real URL)
# and broadcast the asset base to every iframe via postMessage.
#
# This is the fix for the "http://localhost:8501" fallback showing on mobile —
# the parent page always knows the real https://your-app.streamlit.app origin.

BRIDGE_JS = """
<script>
(function() {
  // We are running inside the Streamlit PARENT page, not the game iframe.
  // window.location.origin here is always the real public URL.
  var assetBase = window.location.origin + '/app/static';

  function broadcast() {
    // Target every iframe on the page (there may be several Streamlit iframes)
    var frames = document.querySelectorAll('iframe');
    frames.forEach(function(f) {
      try { f.contentWindow.postMessage({type:'STREAMLIT_ASSET_BASE', url: assetBase}, '*'); }
      catch(e) {}
    });
    // Also broadcast to the parent of THIS iframe in case we're nested
    try { window.parent.postMessage({type:'STREAMLIT_ASSET_BASE', url: assetBase}, '*'); }
    catch(e) {}
  }

  // Reply to any iframe that asks
  window.addEventListener('message', function(e) {
    if (e.data && e.data.type === 'REQUEST_ASSET_BASE') {
      broadcast();
    }
  });

  // Push proactively — the game iframe may already be loaded
  broadcast();
  setTimeout(broadcast, 500);
  setTimeout(broadcast, 1500);
  setTimeout(broadcast, 3000);
})();
</script>
"""

# height=0 + scrolling=False = invisible, zero-height element
st.components.v1.html(BRIDGE_JS, height=0, scrolling=False)

# ─── RENDER GAME ───────────────────────────────────────────────────────────────
# height=10000 ensures the fixed-position iframe is never clipped on short
# mobile viewports (iPhone SE, landscape phones with browser chrome, etc.)
st.components.v1.html(game_html, height=10000, scrolling=False)