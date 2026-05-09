# AI Roblox Companion/Bot System - Complete Build Guide

**Table of Contents**
- [Phase 1: Legal & Ethical Framework](#phase-1-legal--ethical-framework)
- [Phase 2: MVP Architecture](#phase-2-mvp-architecture)
- [Phase 3: Voice Command System](#phase-3-voice-command-system)
- [Phase 4: Roblox NPC Intelligence](#phase-4-roblox-npc-intelligence)
- [Phase 5: Memory & Learning](#phase-5-memory--learning)
- [Phase 6: Human-like Behavior](#phase-6-human-like-behavior-layer)
- [Phase 7: Multi-Bot Squad System](#phase-7-multi-bot-squad-system)
- [Phase 8: Advanced Learning](#phase-8-advanced-learning-later)
- [Phase 9: Folder Structure](#phase-9-full-folder-structure)
- [Phase 10: Code Examples](#phase-10-code-examples)
- [Phase 11: Testing Plan](#phase-11-testing-plan)
- [Phase 12: 30-Day Roadmap](#phase-12-30-day-roadmap)

---

## Phase 1: Legal & Ethical Framework

### What's Allowed vs Not Allowed

**❌ NOT ALLOWED (Will get you banned):**
- Exploiting public Roblox games (unauthorized bots in other games)
- Automating farming, trading, or real-money exploitation
- Cheating in competitive games
- Distributing exploits or injection tools
- Reverse engineering Roblox anti-cheat
- Using bots to bypass account limits or ToS

**✅ ALLOWED (Safe & Legal):**
- Creating your own custom Roblox game with AI NPCs
- Building AI companions in games you own/develop
- Single-player or private server use
- Educational AI experiments in controlled environments
- Open-source tools that require explicit permission to use
- Bots that enhance gameplay (not exploit it)

### The Safest Build Path: Custom Game + AI NPCs

**Step 1: Build Your Own Game First**
```
Your Game (you control)
├── Your AI Companions (you code)
├── Your Custom Rules
└── Your Server/Database

This is the ONLY place to do serious automation.
```

**Why Public-Game Automation is Risky:**
1. **Terms of Service Violation** - Roblox explicitly bans bots in their ToS
2. **Anti-Cheat Detection** - Roblox games use anti-bot detection (pattern recognition, behavior analysis, behavior reporting)
3. **Account Bans** - Account gets permanently banned + flagged
4. **IP Bans** - Severe cases lead to IP-level bans
5. **Legal Risk** - Could violate CFAA (Computer Fraud and Abuse Act)
6. **Community Trust** - Ruins multiplayer experiences

### Recommended Architecture for Safety

```
Tier 1 (Safest): Single-player custom game with AI companions
Tier 2 (Safe): Private Roblox server with friends + AI bots
Tier 3 (Risky): Public game + controlled AI features (with approval)
Tier 4 (Banned): Automating other people's games without permission
```

**Your Path: Tier 1 → Tier 2 → Maybe Tier 3 (with explicit permissions)**

---

## Phase 2: MVP Architecture

### Goal
Create the simplest working AI companion in your own Roblox game.

### What You'll Build
- ✅ Roblox Studio project (your game)
- ✅ One AI NPC companion
- ✅ Follow command
- ✅ Patrol command
- ✅ Attack dummy/enemy command
- ✅ Simple state machine

### Architecture Diagram

```
┌─────────────────────────────────────────┐
│        Roblox Studio Game                │
├─────────────────────────────────────────┤
│                                          │
│  ┌──────────────────────────────────┐  │
│  │  Player (You)                    │  │
│  │  ├─ Position                    │  │
│  │  ├─ Animation                   │  │
│  │  └─ Input Handler               │  │
│  └──────────────────────────────────┘  │
│                                          │
│  ┌──────────────────────────────────┐  │
│  │  AI Companion NPC                │  │
│  │  ├─ State Machine                │  │
│  │  │  ├─ IDLE                      │  │
│  │  │  ├─ FOLLOW                    │  │
│  │  │  ├─ PATROL                    │  │
│  │  │  ├─ ATTACK                    │  │
│  │  │  └─ DEAD                      │  │
│  │  ├─ Humanoid (health, animation)│  │
│  │  ├─ Pathfinding                 │  │
│  │  └─ Behavior Logic              │  │
│  └──────────────────────────────────┘  │
│                                          │
│  ┌──────────────────────────────────┐  │
│  │  Dummy/Enemy Target             │  │
│  │  └─ Health (for testing attack) │  │
│  └──────────────────────────────────┘  │
│                                          │
└─────────────────────────────────────────┘
```

### State Machine Flow

```
        ┌─────────────┐
        │    IDLE     │
        └──────┬──────┘
               │
      ┌────────┼────────┐
      │        │        │
   Command "follow"  "patrol"  "attack"
      │        │        │
      ▼        ▼        ▼
   ┌────────┐┌────────┐┌────────┐
   │ FOLLOW ││ PATROL ││ ATTACK │
   └────┬───┘└───┬────┘└───┬────┘
        │        │         │
        └────────┼─────────┘
                 │
            "stop" command
                 │
                 ▼
           ┌──────────┐
           │   IDLE   │
           └──────────┘
```

### Tech Stack for MVP
- **Game Engine**: Roblox Studio (free, web-based)
- **Scripting Language**: Lua 5.1 (Roblox standard)
- **Physics**: Roblox physics engine (built-in)
- **Network**: Roblox replication system (built-in)
- **Development Time**: ~3-5 days to working MVP

---

## Phase 3: Voice Command System

### Goal
Add voice recognition and command parsing to control the AI companion.

### Architecture

```
┌────────────────────────────────────────────────────┐
│  Local Machine (Your PC)                           │
├────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────┐     ┌──────────────────┐   │
│  │  Microphone      │────▶│ Python Backend   │   │
│  │  (Audio Input)   │     │ Speech-to-Text   │   │
│  └──────────────────┘     │ Command Parser   │   │
│                           │ Intent Detector  │   │
│                           └────────┬─────────┘   │
│                                    │             │
│                                    │             │
│                           ┌────────▼─────────┐   │
│                           │  Roblox Studio   │   │
│                           │  (Game Running)  │   │
│                           │  API Listener    │   │
│                           └──────────────────┘   │
│                                    ▲             │
│                    ┌───────────────┘             │
│                    │                            │
│              HTTP / WebSocket                   │
│                    │                            │
└────────────────────┼────────────────────────────┘
                     │
                     │
┌────────────────────▼────────────────────────────────┐
│  Roblox Server/Game                                 │
├────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────────────────────────────────┐ │
│  │  RemoteFunction: ProcessVoiceCommand()      │ │
│  │  ├─ Input: "follow me"                      │ │
│  │ ├─ Output: { state: "FOLLOW", target: ... } │ │
│  │  └─ Updates AI NPC state                    │ │
│  └──────────────────────────────────────────────┘ │
│                                                     │
└────────────────────────────────────────────────────┘
```

### Voice Commands (Phase 3)

```
Command             Intent              NPC Action
─────────────────────────────────────────────────────
"follow me"         FOLLOW              Move to player position, update every frame
"stop"              STOP                Set state to IDLE, stay in place
"attack"            ATTACK              Attack target dummy
"guard me"          GUARD               Stay near player (follow but 5 studs away)
"patrol"            PATROL              Move between waypoints
"wait here"         WAIT                IDLE state at current position
```

### Tools Needed
- **Speech Recognition**: Google Cloud Speech-to-Text or Vosk (offline)
- **API Communication**: Flask/FastAPI (Python backend) + Roblox HttpService
- **Voice Capture**: Python audio library (pyaudio)
- **Command Parsing**: Regular expressions + keyword matching

### Communication Flow

```
User speaks: "follow me"
    │
    ▼
Microphone captures audio (WAV file)
    │
    ▼
Python speech-to-text: "follow me"
    │
    ▼
Command parser: extract intent="FOLLOW", args={}
    │
    ▼
Validate command (is "FOLLOW" in allowed commands?)
    │
    ▼
Send HTTP POST to Roblox: { intent: "FOLLOW", args: {} }
    │
    ▼
Roblox RemoteFunction processes it
    │
    ▼
Update NPC state machine to FOLLOW
    │
    ▼
NPC starts moving toward player
```

---

## Phase 4: Roblox NPC Intelligence

### Goal
Make the NPC move naturally and react intelligently.

### NPC Core Systems

#### 1. **Pathfinding**
```lua
How it works:
├─ Find path from NPC to target
├─ Avoid obstacles
├─ Navigate around terrain
└─ Update path every 0.5 seconds

Implementation: Use Roblox PathfindingService
```

#### 2. **Target Detection**
```lua
How it works:
├─ Check for enemies within 50 studs
├─ Sort by distance
├─ Pick closest enemy
└─ Update target every 0.2 seconds
```

#### 3. **Line of Sight (LOS)**
```lua
How it works:
├─ Cast ray from NPC to target
├─ If ray hits target → can see
├─ If ray blocked → blocked by terrain
└─ Use for combat decisions
```

#### 4. **Follow Distance**
```lua
How it works:
├─ Player + 5 studs = follow distance
├─ If distance > 10 studs → run
├─ If distance < 5 studs → walk
├─ If distance < 2 studs → stop
```

#### 5. **Obstacle Avoidance**
```lua
How it works:
├─ Cast rays in 8 directions
├─ If ray hits obstacle → turn away
├─ Use humanoid pathfinding
└─ Prevent getting stuck
```

#### 6. **Combat Behavior**
```lua
How it works:
├─ When attacking:
│  ├─ Move within 5 studs of target
│  ├─ Face target
│  ├─ Play attack animation
│  ├─ Damage target
│  └─ Repeat every 1 second
├─ When target dies:
│  ├─ Return to patrol
│  └─ Search for new target
└─ When attacked:
   ├─ Counter-attack
   └─ Call teammate for help (Phase 7)
```

#### 7. **Teammate Behavior**
```lua
How it works:
├─ Know which NPCs are teammates
├─ Help teammates under attack
├─ Share enemy information
└─ Coordinate attacks (Phase 7)
```

### Movement Feel (Not Perfect Robot)

```lua
Normal human behavior:
├─ Walk speed: 16 studs/sec (Roblox humanoid default)
├─ Run speed: 20 studs/sec
├─ Turn smoothly (not instant 180° turns)
├─ Small pause before attacking (0.2-0.5 sec)
├─ Miss target occasionally (80% accuracy)
└─ Get surprised (reaction delay: 0.3-0.8 sec)
```

---

## Phase 5: Memory & Learning

### Goal
Make the NPC remember things and improve over time.

### Memory System Architecture

```
┌─────────────────────────────────────┐
│  NPC Memory System                  │
├─────────────────────────────────────┤
│                                      │
│  ┌────────────────────────────────┐ │
│  │  Short-Term Memory (0-5 min)   │ │
│  │  ├─ Current target position    │ │
│  │  ├─ Last seen player position  │ │
│  │  ├─ Active threats             │ │
│  │  └─ Current objective          │ │
│  └────────────────────────────────┘ │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  Long-Term Memory (lifetime)   │ │
│  │  ├─ Map layout                 │ │
│  │  ├─ Enemy positions (5 min ago)│ │
│  │  ├─ Player behavior patterns   │ │
│  │  ├─ Skill progression          │ │
│  │  └─ Successful strategies      │ │
│  └────────────────────────────────┘ │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  Skill Tracking                │ │
│  │  ├─ Accuracy (hits/attacks)    │ │
│  │  ├─ Pathfinding speed          │ │
│  │  ├─ Combat effectiveness       │ │
│  │  ├─ Team coordination          │ │
│  │  └─ Adaptation rate            │ │
│  └────────────────────────────────┘ │
│                                      │
└─────────────────────────────────────┘
```

### What to Store and Where

#### **Short-Term Memory (in-game variables)**
```lua
{
  currentTarget = player,
  lastPlayerPosition = Vector3.new(10, 5, 20),
  nearbyEnemies = {enemy1, enemy2},
  currentObjective = "FOLLOW",
  timeSinceLastAttack = 0.5,
  healthPercent = 0.8
}
```

#### **Long-Term Memory (local database)**
```json
{
  "npc_id": "Companion_001",
  "lifetime_stats": {
    "total_combat_wins": 12,
    "total_deaths": 2,
    "total_distance_traveled": 5000,
    "accuracy_percent": 85.5
  },
  "map_memory": {
    "safe_zones": [[10, 5, 20], [50, 5, 40]],
    "enemy_spawn_points": [[100, 5, 100]],
    "patrol_routes": [[[0,5,0], [10,5,10], [20,5,0]]]
  },
  "enemy_profiles": {
    "enemy_type_goblin": {
      "typical_health": 50,
      "typical_damage": 10,
      "attack_speed": 2,
      "weakness": "fire"
    }
  },
  "player_behavior": {
    "favorite_location": [25, 5, 30],
    "common_playtime": "6pm-10pm",
    "preferred_tactics": ["ranged_combat", "team_play"]
  },
  "learned_strategies": [
    "when_facing_3_enemies_group_with_player",
    "when_near_fire_zone_use_water_attacks"
  ]
}
```

### Skill Tracking Examples

```lua
-- Every attack
Companion.Stats.TotalAttacks += 1
if hitTarget then
  Companion.Stats.SuccessfulHits += 1
end
Companion.Stats.Accuracy = Companion.Stats.SuccessfulHits / Companion.Stats.TotalAttacks

-- Every patrol complete
Companion.Stats.PatrolsCompleted += 1

-- Every death
Companion.Stats.Deaths += 1
Companion.Stats.SurvivalRate = 1 - (Companion.Stats.Deaths / Companion.Stats.Engagements)

-- Every level/milestone
if Companion.Stats.Accuracy > 0.9 then
  Companion.Level = 2
  Companion.MaxHealth = 150
  Companion.Damage = 12
end
```

### Simple Reinforcement Learning Ideas

```lua
-- Positive feedback: Successful action
if companionWonFight then
  -- Increase weight of "stand and fight" strategy
  strategyWeights["stand_and_fight"] *= 1.1
  
  -- Decrease weight of "run away" strategy
  strategyWeights["run_away"] *= 0.9
end

-- Negative feedback: Failed action
if companionDied then
  -- Decrease weight of strategy that led to death
  strategyWeights[lastStrategy] *= 0.8
  
  -- Normalize weights so they sum to 1
  normalizeWeights(strategyWeights)
end

-- Strategy selection
randomValue = random(0, 1)
cumulativeWeight = 0
for strategy, weight in pairs(strategyWeights) do
  cumulativeWeight += weight
  if randomValue < cumulativeWeight then
    return strategy
  end
end
```

---

## Phase 6: Human-like Behavior Layer

### Goal
Make the NPC feel like a real player, not a perfect bot.

### Realistic Delays

```lua
-- Reaction time (time to process something)
-- Real human: 0.2-0.5 seconds
function NPC:ReactToEvent(event)
  local reactionTime = math.random(200, 500) / 1000  -- 0.2-0.5 sec
  wait(reactionTime)
  self:ProcessEvent(event)
end

-- Combat attack speed
-- Real human: 0.8-1.2 seconds between attacks
function NPC:Attack()
  local attackDelay = math.random(800, 1200) / 1000  -- 0.8-1.2 sec
  while self.State == "ATTACK" do
    self:DealDamage()
    wait(attackDelay)
  end
end

-- Movement start delay
-- Real human: 0.1-0.3 seconds to start moving
function NPC:StartMoving()
  local startDelay = math.random(100, 300) / 1000  -- 0.1-0.3 sec
  wait(startDelay)
  self.Humanoid:MoveTo(targetPosition)
end
```

### Occasional Mistakes

```lua
-- Miss shots occasionally
function NPC:Attack(target)
  local accuracy = 0.85  -- 85% hit rate
  if math.random() > accuracy then
    -- MISS! Damage goes to wrong location
    local offset = Vector3.new(
      math.random(-10, 10),
      math.random(-5, 5),
      math.random(-10, 10)
    )
    self:DealDamage(target.Position + offset)
  else
    self:DealDamage(target.Position)
  end
end

-- Walk into walls occasionally
function NPC:Wander()
  while true do
    local randomDirection = Vector3.new(
      math.random(-100, 100) / 100,
      0,
      math.random(-100, 100) / 100
    )
    local targetPos = self.Position + randomDirection * 20
    
    -- Try to move
    self.Humanoid:MoveTo(targetPos)
    wait(5)
    
    -- If didn't reach target (stuck on wall), pick new direction
    if (self.Position - targetPos).Magnitude > 5 then
      -- Stuck! Reset
    end
  end
end

-- Get distracted occasionally
function NPC:FollowPlayer()
  local followUpdateRate = 0.2  -- Check every 0.2 seconds
  while self.State == "FOLLOW" do
    -- 5% chance to get distracted
    if math.random() < 0.05 then
      wait(1)  -- Stop following for 1 second
    else
      self.Humanoid:MoveTo(self.TargetPlayer.Position)
      wait(followUpdateRate)
    end
  end
end
```

### Natural Movement

```lua
-- Smooth turning (not instant rotations)
function NPC:FaceTarget(target)
  local currentCFrame = self.HumanoidRootPart.CFrame
  local desiredCFrame = CFrame.lookAt(
    self.HumanoidRootPart.Position,
    target.Position
  )
  
  -- Rotate smoothly over 0.3 seconds
  local startTime = tick()
  local duration = 0.3
  
  while tick() - startTime < duration do
    local alpha = (tick() - startTime) / duration
    local newCFrame = currentCFrame:lerp(desiredCFrame, alpha)
    self.HumanoidRootPart.CFrame = newCFrame
    wait(0.05)
  end
end

-- Realistic idle animations
function NPC:IdleAnimation()
  while self.State == "IDLE" do
    -- Look around randomly
    if math.random() < 0.1 then  -- 10% chance per second
      local randomLook = self.Position + Vector3.new(
        math.random(-20, 20),
        math.random(-5, 5),
        math.random(-20, 20)
      )
      self:FaceTarget({ Position = randomLook })
    end
    
    -- Shift weight occasionally (humanoid animation plays automatically)
    wait(1)
  end
end
```

### Hesitation Under Pressure

```lua
function NPC:DecideCombatAction()
  local enemyCount = self:CountNearbyEnemies()
  local healthPercent = self.Humanoid.Health / self.Humanoid.MaxHealth
  
  if enemyCount >= 3 and healthPercent < 0.5 then
    -- Outnumbered and hurt - HESITATE
    local hesitationTime = math.random(500, 2000) / 1000  -- 0.5-2 seconds
    wait(hesitationTime)
  end
  
  -- Decide action
  if healthPercent < 0.3 then
    self:RunAway()
  elseif enemyCount > 2 then
    self:GroupWithPlayer()
  else
    self:Attack()
  end
end

-- Imperfect decision-making
function NPC:ShouldAttack(target)
  -- Perfect AI would always make optimal choice
  -- Realistic NPC: some randomness
  
  local optimalChoice = self:CalculateOptimalAction()
  local randomChoice = self:PickRandomAction()
  
  -- 80% follow optimal, 20% random
  if math.random() < 0.8 then
    return optimalChoice == "ATTACK"
  else
    return randomChoice == "ATTACK"
  end
end
```

---

## Phase 7: Multi-Bot Squad System

### Goal
Manage multiple AI companions with roles and coordination.

### Squad Architecture

```
┌─────────────────────────────────────────┐
│  Squad System                           │
├─────────────────────────────────────────┤
│                                          │
│  Squad: "Team Alpha"                   │
│  ├─ Leader (Tactic manager)            │
│  │  └─ Calls squad commands            │
│  ├─ Scout (Reconnaissance)             │
│  │  └─ Detects enemies early           │
│  ├─ Defender (Tank)                    │
│  │  └─ Absorbs damage                  │
│  ├─ Attacker (DPS)                     │
│  │  └─ High damage output              │
│  └─ Support (Healer)                   │
│     └─ Buffs/heals teammates           │
│                                          │
└─────────────────────────────────────────┘
```

### Squad Member Roles

```lua
ROLES = {
  SCOUT = {
    vision_range = 100,           -- Can see further
    movement_speed = 25,          -- Fastest
    damage = 8,                   -- Lower damage
    armor = 30,                   -- Low defense
    special = "DETECT_ENEMIES"    -- Finds enemies first
  },
  
  DEFENDER = {
    vision_range = 60,
    movement_speed = 16,
    damage = 10,
    armor = 150,                  -- Highest armor
    special = "TAUNT_ENEMIES"     -- Makes enemies attack defender
  },
  
  ATTACKER = {
    vision_range = 70,
    movement_speed = 18,
    damage = 20,                  -- Highest damage
    armor = 60,
    special = "CRITICAL_STRIKE"   -- 30% chance 2x damage
  },
  
  SUPPORT = {
    vision_range = 50,
    movement_speed = 17,
    damage = 5,                   -- Low damage
    armor = 80,
    special = "HEAL_ALLIES"       -- Heals nearby teammates
  }
}
```

### Shared Memory System

```lua
-- Central squad memory
SquadMemory = {
  enemies = {
    {
      id = "enemy_1",
      position = Vector3.new(100, 5, 100),
      health = 45,
      lastSeen = tick(),
      threat_level = "HIGH"
    }
  },
  
  squad_status = {
    leader_position = Vector3.new(0, 5, 0),
    leader_health_percent = 0.8,
    active_members = 4,
    strategy = "HOLD_LINE"
  },
  
  map_data = {
    safe_zones = {...},
    danger_zones = {...},
    enemy_spawn_points = {...}
  }
}

-- All squad members can read/update this memory
function Scout:ReportEnemy(enemy)
  table.insert(SquadMemory.enemies, {
    id = enemy.Name,
    position = enemy.Position,
    health = enemy.Humanoid.Health,
    lastSeen = tick(),
    threat_level = self:CalculateThreatLevel(enemy)
  })
end

function Defender:GetEnemyInfo(enemyId)
  for _, enemy in pairs(SquadMemory.enemies) do
    if enemy.id == enemyId then
      return enemy
    end
  end
end
```

### Squad Commands

```lua
SQUAD_COMMANDS = {
  "HOLD_LINE",        -- Stay in position, fight enemies
  "REGROUP",          -- Come back to leader
  "SPREAD_OUT",       -- Form defensive formation
  "ATTACK_TARGET",    -- Focus fire on specific enemy
  "DEFEND_PLAYER",    -- Protect player position
  "PATROL_AREA",      -- Move around area
  "RETREAT",          -- Fall back to safe zone
  "ADVANCE"           -- Push forward aggressively
}

function Squad:ExecuteCommand(command, args)
  for _, member in pairs(self.Members) do
    if command == "ATTACK_TARGET" then
      member:SetState("ATTACK")
      member:SetTarget(args.target)
    elseif command == "DEFEND_PLAYER" then
      member:SetState("FOLLOW")
      member:SetTarget(args.player)
    elseif command == "HOLD_LINE" then
      member:SetState("IDLE")
      member:MoveTo(args.position)
    end
  end
end
```

### Coordination Logic

```lua
function Squad:CoordinateAttack(targetEnemy)
  -- All members focus on same target
  for _, member in pairs(self.Members) do
    member.Target = targetEnemy
    member.Priority = "ATTACK_TARGET"
  end
  
  -- Scout reports
  self.Scout:ReportEnemy(targetEnemy)
  
  -- Defender taunts
  self.Defender:Taunt(targetEnemy)
  
  -- Wait for taunt to land
  wait(0.5)
  
  -- Everyone attacks
  for _, member in pairs(self.Members) do
    if member.Role ~= "DEFENDER" then  -- Defender tanks
      member:Attack(targetEnemy)
    end
  end
end

function Squad:ReactToMemberDown(member)
  -- Teammate down - react
  self:Announce(member.Name .. " is down!")
  
  -- Support heals them if possible
  if self.Support and not self.Support.InCombat then
    self.Support:MoveTo(member.Position)
    self.Support:HealAlly(member)
  end
  
  -- Others get revenge bonus
  for _, ally in pairs(self.Members) do
    if ally.Name ~= member.Name then
      ally.DamageMultiplier = 1.2  -- 20% damage boost
    end
  end
end
```

---

## Phase 8: Advanced Learning Later

### Future Upgrades (Don't Build These Yet)

#### **Computer Vision**
```python
# Phase 8A: Analyze game screen directly
import cv2
from PIL import ImageGrab

def read_game_screen():
    """Capture game screen and extract info"""
    screenshot = ImageGrab.grab()
    # Detect player health bar location
    # Detect enemy positions on screen
    # Read UI information
    # Return structured game state
    return {
        "player_health": 85,
        "nearby_enemies": [
            {"position": [540, 300], "health": 60}
        ],
        "ui_elements": {...}
    }

# Use for: Auto-targeting, reading health bars, detecting UI
```

#### **UI Reading**
```python
# Phase 8B: OCR + UI parsing
from pytesseract import pytesseract
import numpy as np

def read_game_ui():
    """Extract text from game UI"""
    # Screenshot game
    img = ImageGrab.grab()
    
    # Find and crop UI regions
    health_region = img.crop((10, 10, 100, 50))
    
    # OCR read health text
    health_text = pytesseract.image_to_string(health_region)
    # Parse "Health: 85/100"
    
    return parse_ui_text(health_text)

# Use for: Reading objectives, chat, dialogue, skill cooldowns
```

#### **LLM Reasoning**
```python
# Phase 8C: Use Claude API for decision making
from anthropic import Anthropic

def get_llm_decision(game_state, companion_state):
    """Ask Claude what the companion should do"""
    
    client = Anthropic()
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=100,
        system="""You control an AI game companion.
                 Be tactical, realistic, and avoid perfect play.""",
        messages=[{
            "role": "user",
            "content": f"""Current game state:
            - I'm at position {game_state['player_pos']}
            - Enemy at {game_state['enemy_pos']}, health {game_state['enemy_health']}
            - My health: {companion_state['health']}
            - My mana: {companion_state['mana']}
            
            What should I do? (ATTACK/DEFEND/RUN_AWAY/HEAL)
            Respond with one word only."""
        }]
    )
    
    action = response.content[0].text.strip().upper()
    return action

# Use for: Complex decision making, adaptive tactics, natural reasoning
```

#### **Behavior Trees**
```
# Phase 8D: Complex, modular behavior system
Behavior Tree:
├─ Root
│  ├─ Selector (try each until success)
│  │  ├─ Sequence (all must succeed)
│  │  │  ├─ IsHealthLow() [Condition]
│  │  │  ├─ HealSelf() [Action]
│  │  │  └─ Return SUCCESS
│  │  ├─ Sequence
│  │  │  ├─ IsEnemyNear() [Condition]
│  │  │  ├─ Attack() [Action]
│  │  │  └─ Return SUCCESS
│  │  └─ Patrol() [Default]
```

#### **Reinforcement Learning (Advanced)**
```python
# Phase 8E: Deep learning for tactics
import numpy as np
from tensorflow import keras

class CompanionAI:
    def __init__(self):
        # Neural network that learns from gameplay
        self.model = keras.Sequential([
            keras.layers.Dense(128, activation='relu', input_dim=20),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(8)  # 8 possible actions
        ])
        self.model.compile(optimizer='adam', loss='mse')
    
    def train_from_gameplay(self, game_states, actions, rewards):
        """Learn which actions led to rewards"""
        self.model.fit(game_states, actions, epochs=10)
    
    def decide_action(self, game_state):
        """Predict best action based on training"""
        q_values = self.model.predict(game_state)
        return np.argmax(q_values)  # Pick best action

# Use for: Adaptive tactics that improve over time
```

#### **Game-Specific Adapters**
```python
# Phase 8F: Plugins for different games
class GameAdapter:
    """Override these methods for each game"""
    
    def read_game_state(self):
        """Read from this game's specific UI"""
        raise NotImplementedError
    
    def execute_action(self, action):
        """Execute action in this game's API"""
        raise NotImplementedError
    
    def parse_damage(self, damage_text):
        """Parse damage numbers specific to this game"""
        raise NotImplementedError

class ObroxGameAdapter(GameAdapter):
    def read_game_state(self):
        # Roblox-specific reading
        return self.read_roblox_ui()
    
    def execute_action(self, action):
        # Use Roblox RemoteFunction
        self.invoke_roblox_function(action)
```

#### **Skill Progression**
```
# Phase 8G: Dynamic leveling system
Skill Tree:
├─ Combat
│  ├─ Slash (Level 1)
│  ├─ Power Slash (Level 3) [requires Slash]
│  └─ Whirlwind Attack (Level 5) [requires Power Slash]
├─ Defense
│  ├─ Block (Level 1)
│  ├─ Parry (Level 3)
│  └─ Shield Master (Level 5)
└─ Support
   ├─ Basic Heal (Level 1)
   ├─ Group Heal (Level 3)
   └─ Resurrection (Level 5)

# When companion levels up, unlock new abilities
if companion.xp >= companion.next_level_xp:
    companion.level += 1
    companion.unlock_skills()
```

### Timeline for Phase 8
- **Month 2-3**: Computer vision
- **Month 3**: UI reading
- **Month 3-4**: LLM reasoning
- **Month 4-5**: Behavior trees
- **Month 6+**: Reinforcement learning + game adapters

---

## Phase 9: Full Folder Structure

### Project Layout (Complete)

```
roblox-ai-companion/
│
├── 📁 roblox/                          # Roblox game files
│   ├── place.rbxl                      # Main Roblox place file
│   ├── 📁 ServerScripts/
│   │   ├── init.server.lua             # Game initialization
│   │   ├── npc_manager.server.lua      # NPC spawning/despawning
│   │   ├── api_handler.server.lua      # HTTP API for voice commands
│   │   └── squad_coordinator.server.lua # Squad logic
│   │
│   ├── 📁 LocalScripts/
│   │   ├── input_handler.lua           # Player input
│   │   └── ui_display.lua              # Show NPC state on screen
│   │
│   ├── 📁 Models/
│   │   ├── companion.rbxm              # NPC character model
│   │   ├── enemy_dummy.rbxm            # Test dummy
│   │   └── squad_uniform.rbxm          # Squad member variant
│   │
│   ├── 📁 Animations/
│   │   ├── idle.rbxm                   # Idle animation
│   │   ├── walk.rbxm                   # Walk animation
│   │   ├── run.rbxm                    # Run animation
│   │   ├── attack.rbxm                 # Attack animation
│   │   └── death.rbxm                  # Death animation
│   │
│   └── 📁 Modules/
│       ├── StateMachine.lua            # Core state machine
│       ├── Pathfinding.lua             # Navigation
│       ├── Combat.lua                  # Battle logic
│       ├── Memory.lua                  # NPC memory system
│       ├── BehaviorTree.lua            # Decision making
│       └── Squad.lua                   # Squad management
│
├── 📁 python/                          # Backend server
│   ├── main.py                         # FastAPI app
│   ├── requirements.txt                # Dependencies
│   │
│   ├── 📁 voice/
│   │   ├── speech_to_text.py           # Google/Vosk integration
│   │   ├── command_parser.py           # Intent detection
│   │   └── audio_capture.py            # Microphone input
│   │
│   ├── 📁 roblox_api/
│   │   ├── client.py                   # HTTP client to Roblox
│   │   ├── payloads.py                 # Request/response models
│   │   └── auth.py                     # API authentication
│   │
│   ├── 📁 memory/
│   │   ├── database.py                 # SQLite interface
│   │   ├── schemas.py                  # Memory data structures
│   │   └── queries.py                  # Database queries
│   │
│   ├── 📁 ai/
│   │   ├── decision_engine.py          # Decision making
│   │   ├── llm_interface.py            # Claude API (Phase 8)
│   │   └── computer_vision.py          # Screen reading (Phase 8)
│   │
│   └── 📁 routes/
│       ├── voice_commands.py           # /voice endpoint
│       ├── game_state.py               # /status endpoint
│       └── memory_sync.py              # /memory endpoint
│
├── 📁 config/
│   ├── settings.json                   # Game configuration
│   ├── npc_templates.json              # Preset NPC builds
│   ├── voice_commands.json             # Command definitions
│   └── squad_roles.json                # Role definitions
│
├── 📁 database/
│   ├── companions.db                   # SQLite database
│   ├── migrations/
│   │   ├── 001_init_schema.sql
│   │   └── 002_add_memory_tables.sql
│   └── backups/
│       └── companions_backup.db        # Daily backups
│
├── 📁 logs/
│   ├── app.log                         # Application logs
│   ├── voice_commands.log              # Voice command history
│   ├── npc_behavior.log                # NPC action logs
│   └── errors.log                      # Error logs
│
├── 📁 tests/
│   ├── conftest.py                     # Pytest config
│   ├── test_voice_commands.py          # Voice parsing tests
│   ├── test_npc_logic.py               # Unit tests for Lua logic
│   ├── test_memory_system.py           # Memory tests
│   └── test_integration.py             # End-to-end tests
│
├── 📁 docs/
│   ├── SETUP.md                        # Installation guide
│   ├── API.md                          # API documentation
│   ├── ARCHITECTURE.md                 # System design
│   ├── VOICE_COMMANDS.md               # All voice commands
│   ├── TROUBLESHOOTING.md              # Common issues
│   └── PHASES.md                       # Phase breakdown
│
├── .env.example                        # Environment variables template
├── .gitignore                          # Git ignore rules
├── docker-compose.yml                  # Docker setup
├── README.md                           # Project overview
└── ROADMAP.md                          # Development roadmap
```

### Key File Purposes

```
CRITICAL FILES (build these first):
├── roblox/ServerScripts/init.server.lua     [Phase 2]
├── roblox/Modules/StateMachine.lua          [Phase 2]
├── python/main.py                           [Phase 3]
├── python/voice/command_parser.py           [Phase 3]
├── roblox/Modules/Memory.lua                [Phase 5]
├── config/voice_commands.json               [Phase 3]
└── config/npc_templates.json                [Phase 2]

DATABASE FILES:
├── database/companions.db                   [stores NPC stats]
├── database/migrations/                     [schema versions]
└── logs/                                    [activity history]

CONFIGURATION:
├── config/settings.json                     [game settings]
├── config/squad_roles.json                  [role definitions]
├── .env.example                             [secret template]
└── docker-compose.yml                       [containerization]
```

---

## Phase 10: Code Examples

### 10.1 Roblox Lua: NPC State Machine

**File: `roblox/Modules/StateMachine.lua`**

```lua
local StateMachine = {}
StateMachine.__index = StateMachine

function StateMachine.new(npc)
    local self = setmetatable({}, StateMachine)
    
    self.npc = npc
    self.currentState = "IDLE"
    self.lastStateChange = tick()
    self.stateData = {}
    
    return self
end

function StateMachine:setState(newState, data)
    if newState == self.currentState then
        return
    end
    
    -- Clean up old state
    self:_exitState(self.currentState)
    
    -- Enter new state
    self.currentState = newState
    self.lastStateChange = tick()
    self.stateData = data or {}
    
    self:_enterState(newState)
end

function StateMachine:_enterState(state)
    if state == "IDLE" then
        self.npc:StopMoving()
        self.npc:PlayAnimation("Idle")
        
    elseif state == "FOLLOW" then
        local target = self.stateData.target
        if target then
            self.npc:FollowTarget(target)
        end
        
    elseif state == "PATROL" then
        self.npc:StartPatrol(self.stateData.waypoints)
        
    elseif state == "ATTACK" then
        local enemy = self.stateData.target
        if enemy then
            self.npc:AttackTarget(enemy)
        end
        
    elseif state == "DEAD" then
        self.npc:PlayAnimation("Death")
        self.npc.Humanoid.Health = 0
    end
end

function StateMachine:_exitState(state)
    if state == "ATTACK" then
        self.npc:StopAttacking()
    elseif state == "FOLLOW" then
        self.npc:StopMoving()
    end
end

function StateMachine:update()
    -- Called every frame
    if self.currentState == "FOLLOW" then
        local target = self.stateData.target
        if target and target:IsDescendantOf(workspace) then
            self.npc:UpdateFollowPosition(target.Position)
        else
            self:setState("IDLE")
        end
        
    elseif self.currentState == "ATTACK" then
        local enemy = self.stateData.target
        if enemy and enemy.Humanoid.Health > 0 then
            self.npc:UpdateCombat(enemy)
        else
            self:setState("PATROL")
        end
    end
end

return StateMachine
```

### 10.2 Roblox Lua: Pathfinding & Follow

**File: `roblox/Modules/Pathfinding.lua`**

```lua
local PathfindingService = game:GetService("PathfindingService")
local Pathfinding = {}

function Pathfinding.findPath(npc, targetPos)
    local npcPos = npc.HumanoidRootPart.Position
    
    local waypoints
    local success = pcall(function()
        waypoints = PathfindingService:FindPathAsync(
            npcPos,
            targetPos
        ):GetWaypoints()
    end)
    
    if not success or not waypoints then
        return nil
    end
    
    return waypoints
end

function Pathfinding.followTarget(npc, target)
    if not target or not target:IsDescendantOf(workspace) then
        return
    end
    
    local FOLLOW_DISTANCE = 5
    local UPDATE_RATE = 0.2
    
    while npc.State == "FOLLOW" and target:IsDescendantOf(workspace) do
        local distance = (npc.HumanoidRootPart.Position - target.Position).Magnitude
        
        if distance > FOLLOW_DISTANCE + 5 then
            -- Far away, run
            npc.Humanoid.WalkSpeed = 25
        elseif distance > FOLLOW_DISTANCE then
            -- Normal follow distance, walk
            npc.Humanoid.WalkSpeed = 16
        else
            -- Close enough, stop
            npc.Humanoid:MoveTo(npc.HumanoidRootPart.Position)
            npc.Humanoid.WalkSpeed = 16
        end
        
        -- Move toward target
        npc.Humanoid:MoveTo(target.Position)
        
        wait(UPDATE_RATE)
    end
end

function Pathfinding.patrol(npc, waypoints)
    if not waypoints or #waypoints == 0 then
        return
    end
    
    local currentWaypoint = 1
    npc.Humanoid.WalkSpeed = 16
    
    while npc.State == "PATROL" do
        local waypoint = waypoints[currentWaypoint]
        
        npc.Humanoid:MoveTo(waypoint.Position)
        
        -- Wait until reached waypoint
        while (npc.HumanoidRootPart.Position - waypoint.Position).Magnitude > 5 do
            wait(0.1)
            if npc.State ~= "PATROL" then
                return
            end
        end
        
        -- Random pause at waypoint (0.5-2 seconds)
        wait(math.random(500, 2000) / 1000)
        
        -- Move to next waypoint
        currentWaypoint = currentWaypoint % #waypoints + 1
    end
end

return Pathfinding
```

### 10.3 Python: Voice Command Listener

**File: `python/voice/speech_to_text.py`**

```python
import pyaudio
import wave
from google.cloud import speech_v1

class VoiceListener:
    def __init__(self):
        self.client = speech_v1.SpeechClient()
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 16000
        
    def listen_and_transcribe(self, duration=5):
        """
        Listen to microphone for N seconds and return transcribed text
        
        Args:
            duration: How many seconds to listen
            
        Returns:
            str: Transcribed text or empty string if failed
        """
        audio_data = self._record_audio(duration)
        if not audio_data:
            return ""
        
        text = self._transcribe_audio(audio_data)
        return text.lower()
    
    def _record_audio(self, duration):
        """Record audio from microphone"""
        p = pyaudio.PyAudio()
        
        stream = p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        frames = []
        for _ in range(int(self.RATE / self.CHUNK * duration)):
            data = stream.read(self.CHUNK)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # Save as WAV
        audio_file = wave.open("temp_audio.wav", "wb")
        audio_file.setnchannels(self.CHANNELS)
        audio_file.setsampwidth(p.get_sample_size(self.FORMAT))
        audio_file.setframerate(self.RATE)
        audio_file.writeframes(b''.join(frames))
        audio_file.close()
        
        return "temp_audio.wav"
    
    def _transcribe_audio(self, audio_file):
        """Use Google Speech-to-Text API"""
        with open(audio_file, "rb") as f:
            content = f.read()
        
        audio = speech_v1.RecognitionAudio(content=content)
        config = speech_v1.RecognitionConfig(
            encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.RATE,
            language_code="en-US",
        )
        
        response = self.client.recognize(config=config, audio=audio)
        
        text = ""
        for result in response.results:
            if result.alternatives:
                text = result.alternatives[0].transcript
                break
        
        return text

# Offline alternative using Vosk (no API key needed)
class VoiceListenerOffline:
    def __init__(self):
        from vosk import Model, KaldiRecognizer
        import json
        
        self.model = Model(lang="en-us")
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.p = pyaudio.PyAudio()
        
    def listen_and_transcribe(self, duration=5):
        """Same interface, but offline"""
        stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            samplerate=16000,
            input=True,
            frames_per_buffer=4096
        )
        
        text = ""
        start_time = time.time()
        
        while time.time() - start_time < duration:
            data = stream.read(4096)
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result.get("result", [{}])[0].get("conf", 0)
        
        stream.stop_stream()
        stream.close()
        
        return text.lower()
```

### 10.4 Python: Command Parser

**File: `python/voice/command_parser.py`**

```python
import json
from enum import Enum

class CommandIntent(Enum):
    FOLLOW = "follow"
    STOP = "stop"
    ATTACK = "attack"
    GUARD = "guard"
    PATROL = "patrol"
    WAIT = "wait"
    UNKNOWN = "unknown"

class CommandParser:
    def __init__(self, commands_file="config/voice_commands.json"):
        with open(commands_file, 'r') as f:
            self.command_patterns = json.load(f)
    
    def parse(self, text):
        """
        Parse voice command text into structured command
        
        Args:
            text: Raw voice transcription (lowercase)
            
        Returns:
            dict: { intent: str, args: dict, confidence: float }
        """
        text = text.strip()
        
        # Try exact matches first
        for intent_name, patterns in self.command_patterns.items():
            for pattern in patterns["variations"]:
                if pattern in text:
                    return {
                        "intent": intent_name,
                        "args": {},
                        "confidence": 1.0
                    }
        
        # Try fuzzy matching for variations
        best_match = self._fuzzy_match(text)
        
        if best_match:
            return best_match
        
        return {
            "intent": "unknown",
            "args": {},
            "confidence": 0.0
        }
    
    def _fuzzy_match(self, text):
        """Find closest matching command using string similarity"""
        from difflib import SequenceMatcher
        
        best_match = None
        best_ratio = 0.7  # Minimum confidence threshold
        
        for intent_name, patterns in self.command_patterns.items():
            for pattern in patterns["variations"]:
                ratio = SequenceMatcher(None, text, pattern).ratio()
                
                if ratio > best_ratio:
                    best_match = {
                        "intent": intent_name,
                        "args": {},
                        "confidence": ratio
                    }
                    best_ratio = ratio
        
        return best_match

# config/voice_commands.json
"""
{
  "follow": {
    "variations": [
      "follow me",
      "come with me",
      "follow",
      "come here"
    ]
  },
  "stop": {
    "variations": [
      "stop",
      "wait",
      "wait here",
      "hold on"
    ]
  },
  "attack": {
    "variations": [
      "attack",
      "fight",
      "attack that",
      "kill it"
    ]
  },
  "guard": {
    "variations": [
      "guard me",
      "protect me",
      "stay close"
    ]
  },
  "patrol": {
    "variations": [
      "patrol",
      "patrol area",
      "scout"
    ]
  }
}
"""
```

### 10.5 Python: Roblox API Bridge

**File: `python/roblox_api/client.py`**

```python
import requests
import json
from typing import Dict, Any

class RobloxAPIClient:
    def __init__(self, roblox_server_url="http://localhost:8080"):
        self.base_url = roblox_server_url
        self.timeout = 5
    
    def send_command(self, companion_id: str, command: Dict[str, Any]):
        """
        Send voice command to Roblox NPC
        
        Args:
            companion_id: ID of NPC to control
            command: { "intent": "follow", "args": {} }
        """
        url = f"{self.base_url}/api/command"
        payload = {
            "companion_id": companion_id,
            "command": command,
            "timestamp": time.time()
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to send command: {e}")
            return None
    
    def get_companion_status(self, companion_id: str):
        """Get current NPC state and health"""
        url = f"{self.base_url}/api/companion/{companion_id}/status"
        
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to get status: {e}")
            return None
    
    def sync_memory(self, companion_id: str, memory: Dict[str, Any]):
        """Save companion memory to database"""
        url = f"{self.base_url}/api/companion/{companion_id}/memory"
        
        try:
            response = requests.post(
                url,
                json=memory,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to sync memory: {e}")
            return None
    
    def get_squad_status(self):
        """Get status of all squad members"""
        url = f"{self.base_url}/api/squad/status"
        
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to get squad status: {e}")
            return None
```

### 10.6 Roblox Lua: Server API Handler

**File: `roblox/ServerScripts/api_handler.server.lua`**

```lua
local HttpService = game:GetService("HttpService")
local RunService = game:GetService("RunService")

local API_PORT = 8080
local API_KEY = "your-secret-key"

-- Remote function for voice commands
local ProcessVoiceCommand = Instance.new("RemoteFunction")
ProcessVoiceCommand.Name = "ProcessVoiceCommand"
ProcessVoiceCommand.Parent = game.ServerStorage

function ProcessVoiceCommand.OnServerInvoke(player, command)
    -- command = { intent: "follow", args: {} }
    
    if not command.intent then
        return { success = false, error = "No intent provided" }
    end
    
    -- Find companion NPC
    local companion = workspace:FindFirstChild("Companion")
    if not companion then
        return { success = false, error = "Companion not found" }
    end
    
    -- Execute command
    local success, result = pcall(function()
        return executeCommand(companion, command)
    end)
    
    if success then
        return { success = true, result = result }
    else
        return { success = false, error = result }
    end
end

function executeCommand(companion, command)
    if command.intent == "follow" then
        companion:SetState("FOLLOW", { target = game.Players.LocalPlayer.Character })
        return "Following player"
        
    elseif command.intent == "stop" then
        companion:SetState("IDLE")
        return "Stopped"
        
    elseif command.intent == "attack" then
        local enemy = workspace:FindFirstChild("Enemy")
        if enemy then
            companion:SetState("ATTACK", { target = enemy })
            return "Attacking enemy"
        else
            return "No enemy found"
        end
        
    elseif command.intent == "patrol" then
        companion:SetState("PATROL")
        return "Starting patrol"
        
    else
        return "Unknown command: " .. command.intent
    end
end

-- HTTP endpoint for Python backend
local function startHTTPServer()
    -- Note: Roblox has limited HTTP capabilities
    -- Use RemoteFunction above instead, or run separate HTTP server
    
    -- This is a placeholder - in practice, you'd use FastAPI backend
    -- that calls into Roblox via RemoteFunction
end

-- Listen for commands from Python
local function pollForCommands()
    while true do
        wait(0.5)
        
        -- Check if companion should process pending commands
        -- (commands would be queued by HTTP endpoint)
        if PendingCommands and #PendingCommands > 0 then
            local command = table.remove(PendingCommands, 1)
            ProcessVoiceCommand:InvokeServer(command)
        end
    end
end

spawn(pollForCommands)
```

### 10.7 Python: FastAPI Server (Main Entry Point)

**File: `python/main.py`**

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
import logging

from voice.speech_to_text import VoiceListener
from voice.command_parser import CommandParser
from roblox_api.client import RobloxAPIClient

# Setup
app = FastAPI()
voice_listener = VoiceListener()
command_parser = CommandParser()
roblox_client = RobloxAPIClient()

logger = logging.getLogger(__name__)

# Pydantic models for type safety
class VoiceCommandRequest(BaseModel):
    companion_id: str
    duration: int = 5  # seconds

class CommandRequest(BaseModel):
    companion_id: str
    intent: str
    args: dict = {}

# Routes
@app.post("/api/voice-command")
async def handle_voice_command(request: VoiceCommandRequest):
    """
    Listen to voice, parse command, send to Roblox
    """
    try:
        # Listen to microphone
        print(f"Listening for {request.duration} seconds...")
        text = voice_listener.listen_and_transcribe(request.duration)
        
        if not text:
            return { "error": "No speech detected", "success": False }
        
        logger.info(f"Transcribed: {text}")
        
        # Parse into command
        parsed = command_parser.parse(text)
        
        if parsed["confidence"] < 0.5:
            return {
                "error": f"Command unclear: '{text}'",
                "confidence": parsed["confidence"],
                "success": False
            }
        
        # Send to Roblox
        result = roblox_client.send_command(
            request.companion_id,
            parsed
        )
        
        return {
            "success": True,
            "text": text,
            "intent": parsed["intent"],
            "roblox_result": result
        }
        
    except Exception as e:
        logger.error(f"Voice command error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/command")
async def handle_direct_command(request: CommandRequest):
    """Send direct command to companion (bypass voice)"""
    try:
        result = roblox_client.send_command(
            request.companion_id,
            {
                "intent": request.intent,
                "args": request.args
            }
        )
        return { "success": True, "result": result }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/companion/{companion_id}/status")
async def get_companion_status(companion_id: str):
    """Get NPC status and health"""
    try:
        status = roblox_client.get_companion_status(companion_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Check if server is running"""
    return { "status": "ok" }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 10.8 Python: Memory Storage

**File: `python/memory/database.py`**

```python
import sqlite3
import json
from datetime import datetime

class CompanionMemoryDB:
    def __init__(self, db_path="database/companions.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS companions (
                id TEXT PRIMARY KEY,
                name TEXT,
                level INTEGER DEFAULT 1,
                experience INTEGER DEFAULT 0,
                health INTEGER DEFAULT 100,
                max_health INTEGER DEFAULT 100,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                companion_id TEXT,
                memory_type TEXT,  -- 'enemy', 'map', 'strategy'
                key TEXT,
                value TEXT,  -- JSON encoded
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(companion_id) REFERENCES companions(id)
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                companion_id TEXT,
                stat_name TEXT,  -- 'accuracy', 'wins', 'kills'
                value REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(companion_id) REFERENCES companions(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_memory(self, companion_id, memory_type, key, value):
        """Save a memory entry"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO memory (companion_id, memory_type, key, value)
            VALUES (?, ?, ?, ?)
        ''', (companion_id, memory_type, key, json.dumps(value)))
        
        conn.commit()
        conn.close()
    
    def get_memory(self, companion_id, memory_type, key):
        """Retrieve a memory entry"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            SELECT value FROM memory
            WHERE companion_id = ? AND memory_type = ? AND key = ?
            ORDER BY timestamp DESC LIMIT 1
        ''', (companion_id, memory_type, key))
        
        row = c.fetchone()
        conn.close()
        
        if row:
            return json.loads(row[0])
        return None
    
    def update_stats(self, companion_id, stat_name, value):
        """Update or create a statistic"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO stats (companion_id, stat_name, value)
            VALUES (?, ?, ?)
        ''', (companion_id, stat_name, value))
        
        conn.commit()
        conn.close()
    
    def get_companion_stats(self, companion_id):
        """Get all stats for a companion"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            SELECT stat_name, AVG(value) FROM stats
            WHERE companion_id = ?
            GROUP BY stat_name
        ''', (companion_id,))
        
        stats = {}
        for stat_name, avg_value in c.fetchall():
            stats[stat_name] = avg_value
        
        conn.close()
        return stats
```

---

## Phase 11: Testing Plan

### Testing Checklist

#### **Movement Tests**
```
✅ NPC can walk forward
✅ NPC can run (when target far)
✅ NPC can stop moving
✅ NPC turns smoothly (not instant)
✅ NPC doesn't walk into walls
✅ NPC navigates around obstacles
✅ NPC follows at correct distance (5 studs)
✅ NPC walks slower when close to target
```

#### **Voice Command Tests**
```
✅ Microphone captures audio
✅ Speech-to-text accuracy > 85%
✅ "follow me" → NPC follows
✅ "stop" → NPC stops
✅ "attack" → NPC attacks nearby dummy
✅ "guard me" → NPC stays near player
✅ "patrol" → NPC patrols waypoints
✅ Handle unclear commands (not crash)
✅ Command processing time < 1 second
```

#### **Combat Tests**
```
✅ NPC can attack dummy
✅ NPC deals damage
✅ NPC stops attacking when target dead
✅ NPC takes damage
✅ NPC dies when health reaches 0
✅ NPC plays attack animation
✅ NPC plays death animation
✅ NPC accuracy ~80% (occasional miss)
✅ NPC has realistic attack delays (0.8-1.2 sec)
```

#### **Human-like Behavior Tests**
```
✅ NPC has reaction delay (0.2-0.5 sec)
✅ NPC makes occasional mistakes
✅ NPC doesn't move like a perfect bot
✅ NPC gets distracted sometimes
✅ NPC hesitates under pressure
✅ NPC plays idle animations
✅ NPC looks around randomly
✅ NPC doesn't move instantly
```

#### **Memory & Learning Tests**
```
✅ NPC remembers enemy positions
✅ NPC remembers map layout
✅ NPC updates accuracy stat
✅ NPC improves over time
✅ Memory persists between sessions
✅ Stats persist across games
✅ Can retrieve memory from database
✅ Memory storage doesn't cause lag
```

#### **Multi-Bot Tests**
```
✅ Can spawn multiple NPCs
✅ NPCs don't interfere with each other
✅ Squad commands work
✅ Shared memory updates for all
✅ Roles work (scout, defender, etc.)
✅ Squad coordination works
✅ Teammate detection works
✅ Help teammate when under attack
```

#### **Integration Tests**
```
✅ Voice command → Roblox execution < 2 sec
✅ Python backend stays alive > 1 hour
✅ No memory leaks in Python
✅ No memory leaks in Roblox
✅ Database queries < 100ms
✅ HTTP requests don't timeout
✅ Full game session works (30+ min)
✅ NPC can be respawned
✅ State resets properly on respawn
```

### Testing Command Examples

```bash
# Start backend
python python/main.py

# Test voice command via Python
curl -X POST http://localhost:8000/api/voice-command \
  -H "Content-Type: application/json" \
  -d '{"companion_id": "Companion_001", "duration": 5}'

# Test direct command
curl -X POST http://localhost:8000/api/command \
  -H "Content-Type: application/json" \
  -d '{
    "companion_id": "Companion_001",
    "intent": "follow",
    "args": {}
  }'

# Check status
curl http://localhost:8000/api/companion/Companion_001/status

# Check health
curl http://localhost:8000/api/health
```

---

## Phase 12: 30-Day Roadmap

### Week 1: MVP NPC (Days 1-7)

**Days 1-2: Setup**
- [ ] Create Roblox Studio project
- [ ] Install Python backend (FastAPI)
- [ ] Set up folder structure
- [ ] Create basic database schema
- [ ] Test Python server starts

**Days 3-5: Basic NPC**
- [ ] Create NPC model in Roblox
- [ ] Implement state machine (Lua)
- [ ] Implement humanoid setup
- [ ] Test NPC spawns correctly
- [ ] Implement basic idle state
- [ ] Implement basic walk animation

**Days 6-7: Follow & Patrol**
- [ ] Implement FOLLOW state
- [ ] Test following player
- [ ] Implement PATROL state  
- [ ] Implement pathfinding
- [ ] Add multiple waypoints
- [ ] Test patrol loop

**Deliverable**: NPC that can follow player and patrol

### Week 2: Voice Commands (Days 8-14)

**Days 8-9: Speech Recognition**
- [ ] Set up audio capture (Python)
- [ ] Integrate Google Speech-to-Text
- [ ] Test voice recognition accuracy
- [ ] Handle background noise
- [ ] Cache common commands

**Days 10-11: Command Parsing**
- [ ] Build command parser
- [ ] Define voice command set
- [ ] Test intent detection
- [ ] Handle variations ("follow me", "come here")
- [ ] Implement fuzzy matching

**Days 12-13: Backend API**
- [ ] Create FastAPI endpoints
- [ ] Connect to Roblox via HTTP
- [ ] Implement RemoteFunction handler
- [ ] Test command execution < 1 sec latency
- [ ] Add error handling

**Days 14: Polish**
- [ ] Fix timeout issues
- [ ] Add logging
- [ ] Test full voice→action pipeline
- [ ] Document commands

**Deliverable**: Fully functional voice command system

### Week 3: Combat & Memory (Days 15-21)

**Days 15-17: Combat**
- [ ] Implement ATTACK state
- [ ] Create dummy enemy
- [ ] Implement damage system
- [ ] Add attack animations
- [ ] Test accuracy (~80%)
- [ ] Add reaction delays

**Days 18-19: Memory System**
- [ ] Create memory database schema
- [ ] Implement stat tracking
- [ ] Store enemy/map memory
- [ ] Test persistence
- [ ] Query memory efficiently

**Days 20-21: Learning**
- [ ] Implement accuracy improvement
- [ ] Track combat wins/losses
- [ ] Implement simple RL (strategy weights)
- [ ] Test behavior improves over time
- [ ] Add skill progression

**Deliverable**: NPC that fights, remembers, and improves

### Week 4: Squad & Polish (Days 22-30)

**Days 22-24: Multi-Bot Squad**
- [ ] Spawn multiple NPCs
- [ ] Assign roles (scout, defender, attacker, support)
- [ ] Create shared memory
- [ ] Implement squad commands
- [ ] Test coordination
- [ ] Add squad UI display

**Days 25-27: Advanced Behavior**
- [ ] Add human-like delays
- [ ] Implement occasional mistakes
- [ ] Add hesitation under pressure
- [ ] Improve pathfinding
- [ ] Test natural movement

**Days 28-29: Testing & Fixes**
- [ ] Run full test checklist
- [ ] Fix bugs found
- [ ] Load test (multiple NPCs)
- [ ] Performance optimization
- [ ] Memory leak fixes

**Days 30: Documentation & Demo**
- [ ] Write setup guide
- [ ] Record demo video
- [ ] Create example commands list
- [ ] Document API
- [ ] Prepare for handoff

**Deliverable**: Fully functional AI companion system with squad

### Success Criteria per Week

**Week 1 ✅**
- NPC spawns and follows player smoothly
- No crashes over 30-minute session
- Patrol works with multiple waypoints

**Week 2 ✅**
- Voice commands recognized > 80% accuracy
- Command execution < 1 second latency
- All 6 commands work reliably

**Week 3 ✅**
- Combat system works
- Stats persist in database
- NPC accuracy improves after 20+ fights

**Week 4 ✅**
- 4 NPCs in squad coordinate
- All 8 squad commands work
- Human-like behavior noticeable
- Zero crashes in 2-hour gameplay session

### Contingency Plan

If falling behind:
- **Skip Phase 8** (advanced learning) - can add later
- **Reduce squad members** from 5 to 2
- **Skip computer vision** until Phase 8
- **Use simple waypoints** instead of dynamic pathfinding

If ahead of schedule:
- Add squad formations
- Implement equipment/weapons variety
- Add environment-specific behaviors
- Implement skill trees

---

## Quick Start Guide

### Prerequisites
- **Roblox Studio** (free, web-based)
- **Python 3.9+**
- **Google Cloud credentials** (for speech-to-text) OR Vosk (offline)
- **4GB RAM minimum**

### Installation (5 minutes)

```bash
# Clone repo
git clone https://github.com/yourusername/roblox-ai-companion.git
cd roblox-ai-companion

# Python setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start backend
python python/main.py
# Server runs on http://localhost:8000

# In separate terminal: Start Roblox Studio
# Open roblox/place.rbxl
# Press Play button
# In game, say "follow me" into your microphone
```

### First Voice Command

```
1. Run Python backend (terminal 1)
2. Play game in Roblox Studio (terminal 2)
3. Say: "follow me" into your microphone
4. NPC should start following you
5. Say: "stop" to make them stop
6. Say: "attack" to attack the dummy
```

---

## Glossary

- **NPC**: Non-Player Character (AI companion)
- **State**: What the NPC is currently doing (IDLE, FOLLOW, ATTACK, etc.)
- **Humanoid**: Roblox object that handles health, animations, movement
- **Pathfinding**: Finding route from point A to B
- **RemoteFunction**: Roblox networking tool for client-server communication
- **Reinforcement Learning**: AI learning from successes/failures
- **LLM**: Large Language Model (like Claude)
- **CV/Computer Vision**: Reading game screen visually
- **Behavior Tree**: Structured way to define AI decisions

---

## Additional Resources

- [Roblox Developer Docs](https://developer.roblox.com)
- [Lua 5.1 Reference](https://www.lua.org/manual/5.1/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Google Cloud Speech-to-Text](https://cloud.google.com/speech-to-text)
- [Vosk Offline Speech Recognition](https://alphacephei.com/vosk/)

---

**Version**: 1.0
**Last Updated**: 2026-05-09
**Status**: Complete & Ready to Build

Start with Phase 2 and follow the 30-day roadmap. Good luck!
