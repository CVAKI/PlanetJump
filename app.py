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

# ─── ASSET BASE BRIDGE ────────────────────────────────────────────────────────
# IMPORTANT: st.markdown() strips <script> tags — use st.components.v1.html()
# This tiny invisible iframe runs in the PARENT page (where window.location
# is the real public URL) and broadcasts it down to the game iframe.
BRIDGE_JS = """
<script>
(function() {
  var assetBase = window.location.origin + '/app/static';

  function broadcast() {
    document.querySelectorAll('iframe').forEach(function(f) {
      try { f.contentWindow.postMessage({type:'STREAMLIT_ASSET_BASE', url: assetBase}, '*'); }
      catch(e) {}
    });
    try { window.parent.postMessage({type:'STREAMLIT_ASSET_BASE', url: assetBase}, '*'); }
    catch(e) {}
  }

  window.addEventListener('message', function(e) {
    if (e.data && e.data.type === 'REQUEST_ASSET_BASE') { broadcast(); }
  });

  broadcast();
  setTimeout(broadcast, 500);
  setTimeout(broadcast, 1500);
  setTimeout(broadcast, 3000);
})();
</script>
"""
st.components.v1.html(BRIDGE_JS, height=0, scrolling=False)

# ─── RENDER GAME ───────────────────────────────────────────────────────────────
# height=10000 so the fixed-position iframe is never clipped on mobile
st.components.v1.html(game_html, height=10000, scrolling=False)