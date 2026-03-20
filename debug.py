import streamlit as st
import os

st.set_page_config(page_title="🔍 Debug — Planet Jumpers", layout="wide")

def get_asset_base():
    try:
        headers = dict(st.context.headers)
        host = headers.get("host", "") or headers.get("Host", "")
        proto = headers.get("x-forwarded-proto", "") or headers.get("X-Forwarded-Proto", "")
        if not proto:
            proto = "http" if ("localhost" in host or "127.0.0.1" in host) else "https"
        if host:
            return f"{proto}://{host}/app/static", headers
    except Exception as e:
        return f"ERROR: {e}", {}
    return "UNKNOWN", {}

asset_base, all_headers = get_asset_base()

st.title("🔍 Planet Jumpers — Live Diagnostics")

st.subheader("1️⃣ Python detected asset_base")
st.code(asset_base)

st.subheader("2️⃣ HTTP Request Headers")
st.json(all_headers)

st.subheader("3️⃣ Files on disk")
for path in [
    "game.html",
    ".streamlit/config.toml",
    "static/assets/Sprites/Characters/character_pink_idle.png",
    "static/assets/Sprites/Tiles/terrain_grass_block_top.png",
    "static/assets/Sprites/Enemies/slime_normal_walk_a.png",
    "static/assets/Sprites/Backgrounds/background_color_hills.png",
    "static/assets/Sprites/Tiles/coin_gold.png",
]:
    exists = os.path.exists(path)
    st.write(f"{'✅' if exists else '❌'} `{path}`")

st.subheader("4️⃣ .streamlit/config.toml contents")
if os.path.exists(".streamlit/config.toml"):
    with open(".streamlit/config.toml") as f:
        st.code(f.read(), language="toml")
else:
    st.error("❌ .streamlit/config.toml NOT FOUND")

st.subheader("5️⃣ Browser fetch + image probe  — run on MOBILE")
st.caption("Open this page on your phone. The results will appear inside the box below.")

safe_base = asset_base.replace("'", "\\'").replace('"', '\\"')

PROBE = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  body{margin:0;padding:12px;background:#0d0d1a;color:#e0e0f0;
       font-family:monospace;font-size:13px;}
  .ok{color:#00e676}.fail{color:#ff5252}.info{color:#ffd700}.warn{color:#ff9800}
  .row{padding:4px 0;border-bottom:1px solid #1a1a2e;word-break:break-all}
  h3{color:#ffd700;margin:12px 0 6px}
  .big{font-size:18px;font-weight:bold;margin:10px 0;padding:8px;border-radius:6px}
</style>
</head>
<body>
<h3>Browser Info</h3>
<div class="row info" id="r-origin">loading...</div>
<div class="row info" id="r-ua">loading...</div>
<div class="row info" id="r-base">BASE from Python: __BASE__</div>
<h3>fetch() HTTP Status</h3>
<div id="fetch-out"><div class="row warn">running...</div></div>
<h3>Image() Load Test (same as Phaser)</h3>
<div id="img-out"><div class="row warn">running...</div></div>
<h3>Summary</h3>
<div id="summary" class="big warn">calculating...</div>
<script>
document.getElementById('r-origin').textContent = 'window.origin: ' + window.location.origin;
document.getElementById('r-ua').textContent = 'UA: ' + navigator.userAgent.substring(0, 90);

var BASE = '__BASE__';
var paths = [
  '/assets/Sprites/Characters/character_pink_idle.png',
  '/assets/Sprites/Tiles/terrain_grass_block_top.png',
  '/assets/Sprites/Tiles/coin_gold.png',
  '/assets/Sprites/Enemies/slime_normal_walk_a.png',
  '/assets/Sprites/Backgrounds/background_color_hills.png'
];

var fEl = document.getElementById('fetch-out');
var iEl = document.getElementById('img-out');
var sEl = document.getElementById('summary');
fEl.innerHTML = ''; iEl.innerHTML = '';

var fp=0,ff=0,ip=0,ifl=0,n=paths.length;

function row(parent,msg,cls){
  var d=document.createElement('div');
  d.className='row '+(cls||'');
  d.textContent=msg;
  parent.appendChild(d);
}

function summary(){
  if(fp+ff!==n||ip+ifl!==n) return;
  if(ip===n){
    sEl.className='big ok';
    sEl.textContent='ALL '+n+' ASSETS LOADED OK - sprites should show in game';
  } else {
    sEl.className='big fail';
    sEl.textContent='FAILED: fetch='+fp+'/'+n+' ok, image='+ip+'/'+n+' ok';
    if(fp===n && ifl>0)
      row(sEl.parentNode,'Files exist (fetch 200) but Image() fails = CORS/CSP inside iframe','warn');
    else if(ff>0)
      row(sEl.parentNode,'HTTP errors = wrong URL or enableStaticServing not working','fail');
  }
}

paths.forEach(function(p){
  var url=BASE+p+'?t='+Date.now();
  fetch(url,{method:'HEAD',cache:'no-store'})
    .then(function(r){
      if(r.ok){fp++;row(fEl,'HTTP '+r.status+' OK  '+p,'ok');}
      else{ff++;row(fEl,'HTTP '+r.status+' FAIL  '+url,'fail');}
      summary();
    })
    .catch(function(e){ff++;row(fEl,'NETWORK ERR: '+e+'  '+url,'fail');summary();});

  var img=new Image();
  img.onload=function(){ip++;row(iEl,img.naturalWidth+'x'+img.naturalHeight+' OK  '+p,'ok');summary();};
  img.onerror=function(){ifl++;row(iEl,'FAILED  '+url,'fail');summary();};
  img.src=url;
});
</script>
</body>
</html>""".replace("__BASE__", safe_base)

st.components.v1.html(PROBE, height=700, scrolling=True)

st.subheader("6️⃣ Paste these into your mobile browser address bar")
for path in ["/assets/Sprites/Characters/character_pink_idle.png",
             "/assets/Sprites/Tiles/coin_gold.png"]:
    st.code(asset_base + path)