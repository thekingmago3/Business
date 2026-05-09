# AI Kingdom - Quick Start Guide

## Today's Build: Foundation Complete ✅

You now have everything you need to build the **AI Medieval Kingdom Foundation** in about 2-3 hours.

---

## What You Have

📋 **AI_KINGDOM_FOUNDATION.md** - Step-by-step implementation guide (FOLLOW THIS)
📁 **python/ai_kingdom_main.py** - Backend server code (ready to run)
⚙️ **config/npcs.json** - NPC configuration
📦 **python/requirements.txt** - Python dependencies

---

## Quick Start (2-3 hours)

### Step 1: Open the Guide
Open **AI_KINGDOM_FOUNDATION.md** and follow it exactly.

The guide walks you through:
1. Setting up Roblox Studio (10 min)
2. Setting up Python backend (10 min)
3. Creating Lua NPC code (copy-paste, 30 min)
4. Creating world in Roblox (30 min)
5. Testing (20 min)

### Step 2: Python Backend (Optional but Recommended)

If you want the backend running:

```bash
cd python
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
python ai_kingdom_main.py
```

Server will run on: http://localhost:8000

### Step 3: Test Your Game

In Roblox Studio:
- Press Play
- Press F to make NPC follow
- Press P to make NPC patrol
- Press S to make NPC stop

---

## File Structure

```
Business/
├── AI_KINGDOM_FOUNDATION.md      👈 START HERE
├── QUICK_START.md                (this file)
├── config/
│   └── npcs.json                 (NPC definitions)
└── python/
    ├── ai_kingdom_main.py         (backend server)
    ├── requirements.txt           (python packages)
    └── (other files)
```

---

## Expected Result After Today

✅ Roblox game with medieval world
✅ 5 NPCs with personalities
✅ NPC AI that patrols, idles, and follows
✅ Player controls (F, P, S keys)
✅ Backend server running (optional)

---

## Next Steps (After Today)

Once the foundation is working:

**Week 2**: Add relationships and communication
- NPCs talk to each other
- NPCs like/dislike each other
- NPCs remember players

**Week 3**: Add combat and learning
- NPCs fight each other
- NPCs improve from experience
- Stat progression

**Week 4**: Add squad system
- Recruit NPCs as teammates
- Give squad commands
- Multi-NPC coordination

---

## Troubleshooting

**"NPC won't move"**
- Check ServerScriptService has NPCSpawner
- Check ServerStorage has NPCController module
- Check console for errors

**"Controls don't work"**
- Make sure PlayerCommands is in StarterCharacterScripts
- Press F while in game (not in menu)

**"Python won't start"**
- Make sure Python 3.9+ is installed
- Check virtual environment is activated
- pip install -r requirements.txt completed

---

## Support

If you get stuck:
1. Check the console in Roblox (View > Output)
2. Check the Python terminal for errors
3. Re-read the specific section in AI_KINGDOM_FOUNDATION.md
4. All error messages tell you what's wrong

---

## You're Building Something Cool

You're creating an AI ecosystem with:
- Emergent behavior
- Learning systems
- Social interactions
- Player interaction
- Living world

This is legitimately impressive. Take your time, follow the guide exactly, and you'll have something working by tonight.

Good luck! 🏰✨
