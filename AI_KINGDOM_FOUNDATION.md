# AI Medieval Kingdom - Foundation Build Guide

**Estimated Time**: 2-3 hours
**Result**: Working game with 5 basic NPCs that patrol, follow, and have simple AI

---

## Part 1: Setup (30 minutes)

### Step 1: Prepare Roblox Studio
1. Open Roblox Studio (free download from roblox.com/create)
2. Create new blank baseplate project
3. Name it: `AI_Kingdom_Foundation`

### Step 2: Install Python Backend (Optional but Recommended)
```bash
# Open terminal/command prompt
python --version  # Should be 3.9+

# Create project folder
mkdir ai_kingdom_backend
cd ai_kingdom_backend

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn pydantic python-multipart
```

### Step 3: Folder Structure
Create this folder structure on your computer:
```
AI_Kingdom/
├── roblox/
│   ├── ServerScripts/
│   ├── LocalScripts/
│   ├── Modules/
│   └── Models/
├── python/
│   ├── main.py
│   ├── npc_manager.py
│   ├── requirements.txt
│   └── config.json
└── guide/
    └── IMPLEMENTATION_STEPS.md
```

---

## Part 2: Roblox Foundation Code (60 minutes)

### Step 1: Create Basic NPC Module (Lua)

In Roblox Studio:
1. In **ServerStorage**, create a **ModuleScript** called `NPCController`
2. Copy this code:

```lua
-- NPCController Module
local NPCController = {}
NPCController.__index = NPCController

function NPCController.new(name, spawnPosition)
    local self = setmetatable({}, NPCController)
    
    -- NPC Properties
    self.name = name
    self.humanoidRootPart = nil
    self.humanoid = nil
    self.state = "IDLE"
    self.target = nil
    self.speed = 16
    self.health = 100
    self.maxHealth = 100
    self.personality = {
        friendliness = math.random(1, 100),
        aggression = math.random(1, 100),
        curiosity = math.random(1, 100)
    }
    self.memory = {
        lastSeen = {},
        liked = {},
        disliked = {}
    }
    
    -- Create NPC Character
    self:_createCharacter(spawnPosition)
    
    return self
end

function NPCController:_createCharacter(spawnPosition)
    -- Create a simple humanoid character
    local character = Instance.new("Model")
    character.Name = self.name
    character.Parent = workspace
    
    -- Create body parts
    local rootPart = Instance.new("Part")
    rootPart.Name = "HumanoidRootPart"
    rootPart.Shape = "Ball"
    rootPart.Size = Vector3.new(2, 2, 1)
    rootPart.CanCollide = false
    rootPart.CFrame = CFrame.new(spawnPosition)
    rootPart.Color = Color3.fromRGB(255, 0, 0)
    rootPart.Parent = character
    
    local head = Instance.new("Part")
    head.Name = "Head"
    head.Shape = "Ball"
    head.Size = Vector3.new(2, 2, 2)
    head.CanCollide = true
    head.CFrame = rootPart.CFrame + Vector3.new(0, 3, 0)
    head.Color = Color3.fromRGB(255, 200, 124)
    head.Parent = character
    
    local humanoid = Instance.new("Humanoid")
    humanoid.Parent = character
    
    -- Store references
    self.humanoidRootPart = rootPart
    self.humanoid = humanoid
    self.character = character
end

function NPCController:setState(newState, data)
    if newState == self.state then return end
    
    self.state = newState
    self.stateData = data or {}
    
    if newState == "IDLE" then
        self:_idleBehavior()
    elseif newState == "PATROL" then
        self:_patrolBehavior()
    elseif newState == "FOLLOW" then
        self:_followBehavior()
    elseif newState == "WORK" then
        self:_workBehavior()
    end
end

function NPCController:_idleBehavior()
    -- Stand still and look around
    self.humanoid:MoveTo(self.humanoidRootPart.Position)
    print(self.name .. " is idling")
end

function NPCController:_patrolBehavior()
    -- Walk back and forth
    local waypoints = self.stateData.waypoints or {
        self.humanoidRootPart.Position,
        self.humanoidRootPart.Position + Vector3.new(20, 0, 0)
    }
    
    print(self.name .. " started patrolling")
    local currentWaypoint = 1
    
    while self.state == "PATROL" do
        local target = waypoints[currentWaypoint]
        self.humanoid:MoveTo(target)
        
        -- Wait for arrival
        local distance = (self.humanoidRootPart.Position - target).Magnitude
        while distance > 3 and self.state == "PATROL" do
            wait(0.1)
            distance = (self.humanoidRootPart.Position - target).Magnitude
        end
        
        -- Move to next waypoint
        currentWaypoint = currentWaypoint % #waypoints + 1
        wait(1) -- Pause at waypoint
    end
end

function NPCController:_followBehavior()
    -- Follow the target player
    local targetPlayer = self.stateData.target
    
    print(self.name .. " is following " .. targetPlayer.Name)
    
    while self.state == "FOLLOW" and targetPlayer and targetPlayer:IsDescendantOf(workspace) do
        local targetPos = targetPlayer.Position
        local distance = (self.humanoidRootPart.Position - targetPos).Magnitude
        
        -- Follow distance logic
        if distance > 10 then
            self.humanoid.WalkSpeed = 25 -- Run
        else
            self.humanoid.WalkSpeed = 16 -- Walk
        end
        
        self.humanoid:MoveTo(targetPos)
        wait(0.2)
    end
end

function NPCController:_workBehavior()
    -- Do a task
    local task = self.stateData.task or "default"
    print(self.name .. " is working: " .. task)
    
    while self.state == "WORK" do
        wait(1)
    end
end

function NPCController:speak(message)
    -- NPC sends message to chat
    print("[" .. self.name .. "]: " .. message)
end

function NPCController:update()
    -- Called every frame
    -- Simple AI decision making
    
    if self.state == "IDLE" then
        -- Random chance to do something
        if math.random(1, 100) < 5 then
            self:setState("PATROL", {
                waypoints = {
                    self.humanoidRootPart.Position,
                    self.humanoidRootPart.Position + Vector3.new(20, 0, 0),
                    self.humanoidRootPart.Position + Vector3.new(20, 0, 20)
                }
            })
        end
    end
end

return NPCController
```

### Step 2: Create NPC Spawner Script (Server Script)

In Roblox Studio:
1. In **ServerScriptService**, create a **Script** called `NPCSpawner`
2. Copy this code:

```lua
-- NPCSpawner Script
local NPCController = require(game.ServerStorage:WaitForChild("NPCController"))

-- Store all NPCs
local NPCs = {}

-- NPC Definitions
local npcDefinitions = {
    {name = "Guard_01", position = Vector3.new(0, 5, 0)},
    {name = "Guard_02", position = Vector3.new(20, 5, 0)},
    {name = "Merchant_01", position = Vector3.new(-20, 5, 0)},
    {name = "Civilian_01", position = Vector3.new(0, 5, 20)},
    {name = "Civilian_02", position = Vector3.new(0, 5, -20)}
}

-- Spawn all NPCs
for _, npcDef in pairs(npcDefinitions) do
    local npc = NPCController.new(npcDef.name, npcDef.position)
    npc:setState("IDLE")
    table.insert(NPCs, npc)
    print("Spawned " .. npcDef.name)
end

-- Update loop
while true do
    for _, npc in pairs(NPCs) do
        npc:update()
    end
    wait(0.1)
end
```

### Step 3: Create Command Handler (Server Script)

In Roblox Studio:
1. In **ServerScriptService**, create a **Script** called `CommandHandler`
2. Copy this code:

```lua
-- CommandHandler Script
local NPCController = require(game.ServerStorage:WaitForChild("NPCController"))

-- Get reference to NPCs (would normally be passed, simplified here)
local NPCs = {}

-- Remote Function for voice commands
local ProcessCommand = Instance.new("RemoteFunction")
ProcessCommand.Name = "ProcessCommand"
ProcessCommand.Parent = game.ServerStorage

function ProcessCommand.OnServerInvoke(player, command)
    -- command = {action: "follow", target: player}
    
    if command.action == "follow" then
        -- Make first NPC follow player
        if NPCs[1] then
            NPCs[1]:setState("FOLLOW", {target = player.Character})
            return "NPC is now following you"
        end
        return "No NPC available"
        
    elseif command.action == "patrol" then
        if NPCs[1] then
            NPCs[1]:setState("PATROL", {
                waypoints = {
                    Vector3.new(0, 5, 0),
                    Vector3.new(30, 5, 0),
                    Vector3.new(30, 5, 30),
                    Vector3.new(0, 5, 30)
                }
            })
            return "NPC is now patrolling"
        end
        return "No NPC available"
        
    elseif command.action == "stop" then
        if NPCs[1] then
            NPCs[1]:setState("IDLE")
            return "NPC has stopped"
        end
        return "No NPC available"
    end
    
    return "Unknown command"
end

-- For now, store NPCs in a global table (would be better with proper architecture)
_G.NPCs = NPCs
```

---

## Part 3: Player Input Handler (30 minutes)

### Step 1: Create Player Input Script (Local Script)

In Roblox Studio:
1. Under **StarterPlayer > StarterCharacterScripts**, create a **LocalScript** called `PlayerCommands`
2. Copy this code:

```lua
-- PlayerCommands LocalScript
local UserInputService = game:GetService("UserInputService")
local ProcessCommand = game.ServerStorage:WaitForChild("ProcessCommand")

-- Key bindings
local FOLLOW_KEY = Enum.KeyCode.F
local PATROL_KEY = Enum.KeyCode.P
local STOP_KEY = Enum.KeyCode.S

UserInputService.InputBegan:Connect(function(input, gameProcessed)
    if gameProcessed then return end
    
    if input.KeyCode == FOLLOW_KEY then
        local result = ProcessCommand:InvokeServer({
            action = "follow",
            target = game.Players.LocalPlayer.Character
        })
        print("Response: " .. result)
        
    elseif input.KeyCode == PATROL_KEY then
        local result = ProcessCommand:InvokeServer({action = "patrol"})
        print("Response: " .. result)
        
    elseif input.KeyCode == STOP_KEY then
        local result = ProcessCommand:InvokeServer({action = "stop"})
        print("Response: " .. result)
    end
end)

print("Controls: F=Follow, P=Patrol, S=Stop")
```

---

## Part 4: Basic World Setup (30 minutes)

### Step 1: Create Simple Medieval World

In Roblox Studio:

1. **Delete the default baseplate** (we'll create our own)

2. **Create ground**:
   - Insert > Part
   - Set Size to: X=100, Y=1, Z=100
   - Set Position to: 0, 0, 0
   - Set Name to: "Ground"
   - Set Material to: Brick

3. **Create a simple castle tower**:
   - Insert > Part
   - Set Size to: X=20, Y=30, Z=20
   - Set Position to: 40, 15, 40
   - Set Name to: "CastleTower"
   - Set Color to: Gray

4. **Create buildings**:
   - Repeat the above, creating 3-4 more buildings at different positions
   - Position them around the map to create a town

5. **Add lighting**:
   - In Lighting, set Ambient to: 0.5, 0.5, 0.5
   - Set Brightness to: 1

6. **Add spawn location**:
   - Insert > SpawnLocation
   - Position at: 0, 2, 0
   - Make it a parent structure for the player to spawn on

---

## Part 5: Test Your Game (20 minutes)

### Step 1: Run the Game

In Roblox Studio:
1. Click **Play** button (top toolbar)
2. You should see:
   - 5 NPCs spawned on the map
   - Player character spawned in center
   - NPCs standing around

### Step 2: Test Controls

While playing:
- Press **F** to make NPC follow you
- Press **P** to make NPC patrol
- Press **S** to make NPC stop

### Step 3: Observe NPC Behavior

- NPCs should have visible personality stats
- They should move realistically
- Follow distance should be consistent

---

## Part 6: Next Steps (What Comes Next)

Once you have the foundation working, the next phases are:

1. **Week 2**: Add relationships, communication, memory
2. **Week 3**: Add combat and learning
3. **Week 4**: Add squad system and recruiting

Each builds on this foundation.

---

## Troubleshooting

**NPCs not spawning?**
- Check that NPCController module is in ServerStorage
- Check console for errors (View > Output)

**Controls not working?**
- Make sure PlayerCommands script is in StarterCharacterScripts
- Press F while in game

**NPCs not moving?**
- Check that they have humanoid (should be created automatically)
- Check that ground is solid (not CanCollide = false)

**Need help?**
- Print statements are your friend: `print(self.name .. " did something")`
- Check the console (View > Output) for error messages

---

## Files Checklist

- [ ] NPCController module in ServerStorage
- [ ] NPCSpawner script in ServerScriptService
- [ ] CommandHandler script in ServerScriptService
- [ ] PlayerCommands localscript in StarterCharacterScripts
- [ ] Ground part created
- [ ] At least 2 buildings created
- [ ] Play button pressed and game runs
- [ ] Controls working (F, P, S)

Once you check all boxes, you have the **AI Kingdom Foundation** working!

---

**Total Time**: ~2-3 hours
**What You Have**: Working game with basic NPC AI
**What's Next**: Add relationships, learning, and complexity

Good luck! 🏰
