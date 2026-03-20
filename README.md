# 🪐 Planet Jumpers: Coin Rush
### Real-time Multiplayer Platformer — Built with Phaser 3, Firebase & Streamlit

---

## 📦 Project Structure

```
planetjumpers/
├── app.py                   ← Streamlit entry point
├── game.html                ← Phaser 3 game (source copy)
├── requirements.txt
├── .streamlit/
│   └── config.toml          ← Enables static file serving
├── static/
│   ├── game.html            ← Served game file
│   └── assets/              ← Kenney Platformer Art (included)
│       ├── Sprites/
│       │   ├── Characters/
│       │   ├── Tiles/
│       │   ├── Enemies/
│       │   └── Backgrounds/
│       ├── Sounds/
│       └── Spritesheets/
└── README.md
```

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install streamlit
```

### 2. Run the game
```bash
streamlit run app.py
```

### 3. Open in browser
Navigate to `http://localhost:8501`

---

## 🎮 How to Play

### Lobby
1. **Enter your name** and choose a character color
2. **Create Room** — share the 6-letter code with friends
3. **Join Room** — enter a room code to join
4. Host clicks **Start Game** when ready (1–10 players)

### Controls

| Platform | Left | Right | Jump |
|----------|------|-------|------|
| Desktop  | ← / A | → / D | ↑ / W / Space |
| Mobile   | ◀ button | ▶ button | ⬆ button |

### Scoring

| Action | Points |
|--------|--------|
| 🥇 Gold Coin | 3 pts |
| 🥈 Silver Coin | 2 pts |
| 🥉 Bronze Coin | 1 pt |
| 👟 Stomp Enemy | 2 pts |
| **Win target** | **20 pts** |

### Tips
- **Stomp enemies** by jumping and landing on top of them for bonus points
- **Fall off the screen** and you lose a life (respawn at 3 lives)
- Coins **bob up and down** — collect them all before other players!

---

## 🌐 Deploy to Streamlit Cloud

1. Push this folder to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set **Main file path** to `app.py`
4. Deploy!

> ⚠️ Make sure the `static/` folder (with `assets/` and `game.html`) is committed to your repo.

---

## 🔧 Firebase Setup

The game uses Firebase Realtime Database for multiplayer. The config is already included.
- **Database rules** should allow read/write for game to work
- Rooms auto-clean up when all players disconnect

Recommended Firebase rules (set in Firebase Console):
```json
{
  "rules": {
    "rooms": {
      "$roomId": {
        ".read": true,
        ".write": true
      }
    }
  }
}
```

---

## 🎨 Assets

All game art is from the [Kenney Platformer Art Deluxe](https://kenney.nl) pack (CC0 Public Domain).
- 5 character colors: Pink, Beige, Green, Purple, Yellow
- Grass terrain tiles, cloud platforms, ledges
- Gold/Silver/Bronze coins
- Slime and Ladybug enemies
- Colorful hill backgrounds

---

*Made with ❤️ using Phaser 3, Firebase Realtime Database, and Streamlit*
