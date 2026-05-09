"""
AI Kingdom Backend - Main Server
Handles NPC management, learning, and game state
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(title="AI Kingdom Backend")

# ============================================
# Data Models
# ============================================

class NPCState(BaseModel):
    npc_id: str
    name: str
    position: List[float]
    state: str  # IDLE, PATROL, FOLLOW, WORK
    health: int
    personality: Dict[str, int]
    memory: Dict

class CommandRequest(BaseModel):
    action: str
    npc_id: str
    data: Optional[Dict] = {}

class NPCResponse(BaseModel):
    success: bool
    message: str
    npc_state: Optional[NPCState] = None

# ============================================
# NPC Manager
# ============================================

class NPCManager:
    """Manages all NPCs in the game"""

    def __init__(self):
        self.npcs = {}
        self.load_npc_data()

    def load_npc_data(self):
        """Load NPC data from config"""
        try:
            with open("config/npcs.json", "r") as f:
                npc_configs = json.load(f)
                for config in npc_configs:
                    self.create_npc(config)
                logger.info(f"Loaded {len(self.npcs)} NPCs")
        except FileNotFoundError:
            logger.warning("No NPC config found, starting with empty")

    def create_npc(self, config):
        """Create a new NPC"""
        npc = {
            "id": config.get("id"),
            "name": config.get("name"),
            "position": config.get("position", [0, 5, 0]),
            "state": "IDLE",
            "health": 100,
            "max_health": 100,
            "personality": {
                "friendliness": config.get("friendliness", 50),
                "aggression": config.get("aggression", 50),
                "curiosity": config.get("curiosity", 50)
            },
            "memory": {
                "last_seen": {},
                "liked": {},
                "disliked": {},
                "skills": {},
                "experiences": []
            },
            "stats": {
                "total_interactions": 0,
                "total_fights": 0,
                "wins": 0,
                "level": 1,
                "experience": 0
            }
        }
        self.npcs[config.get("id")] = npc
        return npc

    def get_npc(self, npc_id):
        """Get NPC by ID"""
        if npc_id not in self.npcs:
            raise ValueError(f"NPC {npc_id} not found")
        return self.npcs[npc_id]

    def update_npc_state(self, npc_id, new_state, data=None):
        """Update NPC state"""
        npc = self.get_npc(npc_id)
        npc["state"] = new_state
        npc["state_data"] = data or {}
        logger.info(f"{npc['name']} state changed to {new_state}")
        return npc

    def add_to_memory(self, npc_id, memory_type, key, value):
        """Add something to NPC memory"""
        npc = self.get_npc(npc_id)
        npc["memory"][memory_type][key] = value
        logger.info(f"Added to {npc['name']}'s memory: {key}")

    def get_all_npcs(self):
        """Get all NPCs"""
        return list(self.npcs.values())

    def save_npc_data(self):
        """Save NPC data to file"""
        try:
            with open("config/npcs.json", "w") as f:
                json.dump(list(self.npcs.values()), f, indent=2)
            logger.info("NPC data saved")
        except Exception as e:
            logger.error(f"Failed to save NPC data: {e}")

# Initialize NPC Manager
npc_manager = NPCManager()

# ============================================
# API Endpoints
# ============================================

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "ok",
        "service": "AI Kingdom Backend",
        "npcs_count": len(npc_manager.npcs)
    }

@app.get("/api/npcs")
async def get_all_npcs():
    """Get all NPCs"""
    return {"npcs": npc_manager.get_all_npcs()}

@app.get("/api/npc/{npc_id}")
async def get_npc(npc_id: str):
    """Get specific NPC"""
    try:
        npc = npc_manager.get_npc(npc_id)
        return {"npc": npc}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/command")
async def send_command(command: CommandRequest):
    """Send command to NPC"""
    try:
        npc = npc_manager.get_npc(command.npc_id)

        if command.action == "follow":
            npc_manager.update_npc_state(
                command.npc_id,
                "FOLLOW",
                command.data
            )
            return NPCResponse(
                success=True,
                message=f"{npc['name']} is now following",
                npc_state=NPCState(**npc)
            )

        elif command.action == "patrol":
            npc_manager.update_npc_state(
                command.npc_id,
                "PATROL",
                command.data
            )
            return NPCResponse(
                success=True,
                message=f"{npc['name']} started patrolling",
                npc_state=NPCState(**npc)
            )

        elif command.action == "stop":
            npc_manager.update_npc_state(command.npc_id, "IDLE")
            return NPCResponse(
                success=True,
                message=f"{npc['name']} stopped",
                npc_state=NPCState(**npc)
            )

        else:
            raise HTTPException(status_code=400, detail="Unknown command")

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Command error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/npc/{npc_id}/memory")
async def add_memory(npc_id: str, memory_data: Dict):
    """Add to NPC memory"""
    try:
        npc = npc_manager.get_npc(npc_id)

        memory_type = memory_data.get("type", "experience")
        key = memory_data.get("key")
        value = memory_data.get("value")

        npc_manager.add_to_memory(npc_id, memory_type, key, value)

        return {
            "success": True,
            "message": f"Memory added to {npc['name']}",
            "npc": npc
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/npc/{npc_id}/stats")
async def update_stats(npc_id: str, stats: Dict):
    """Update NPC stats"""
    try:
        npc = npc_manager.get_npc(npc_id)

        for key, value in stats.items():
            npc["stats"][key] = value

        logger.info(f"Updated stats for {npc['name']}")

        return {
            "success": True,
            "message": f"Stats updated for {npc['name']}",
            "stats": npc["stats"]
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check"""
    return {"status": "ok", "service": "AI Kingdom Backend"}

# ============================================
# Shutdown handler
# ============================================

@app.on_event("shutdown")
async def shutdown_event():
    """Save data on shutdown"""
    logger.info("Saving NPC data...")
    npc_manager.save_npc_data()
    logger.info("Shutdown complete")

# ============================================
# Run the server
# ============================================

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting AI Kingdom Backend...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
