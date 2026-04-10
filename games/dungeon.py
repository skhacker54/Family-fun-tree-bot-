"""
Dungeon Crawler for Fam Tree Bot
=================================
Procedurally generated dungeon exploration
"""

import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

@dataclass
class DungeonRoom:
    """Dungeon room"""
    x: int
    y: int
    room_type: str  # empty, monster, treasure, trap, boss, entrance, exit
    visited: bool = False
    contents: Dict = field(default_factory=dict)

@dataclass
class DungeonMonster:
    """Dungeon monster"""
    name: str
    hp: int
    max_hp: int
    attack: int
    defense: int
    xp_reward: int
    gold_reward: int

class DungeonCrawler:
    """Main dungeon crawler class"""
    
    MONSTERS = {
        "goblin": DungeonMonster("Goblin", 30, 30, 8, 3, 10, 15),
        "skeleton": DungeonMonster("Skeleton", 40, 40, 10, 5, 15, 20),
        "orc": DungeonMonster("Orc", 60, 60, 15, 8, 25, 35),
        "troll": DungeonMonster("Troll", 100, 100, 20, 12, 50, 60),
        "dragon": DungeonMonster("Dragon", 200, 200, 35, 20, 200, 500),
    }
    
    TREASURE_ITEMS = [
        {"name": "Health Potion", "type": "consumable", "effect": "heal", "value": 30},
        {"name": "Mana Potion", "type": "consumable", "effect": "mana", "value": 20},
        {"name": "Gold Coins", "type": "gold", "value": 50},
        {"name": "Ancient Sword", "type": "weapon", "attack": 10},
        {"name": "Steel Armor", "type": "armor", "defense": 8},
        {"name": "Magic Ring", "type": "accessory", "magic": 5},
    ]
    
    def __init__(self, player_id: int, size: int = 5):
        self.player_id = player_id
        self.size = size
        self.grid: List[List[DungeonRoom]] = []
        self.player_pos = (0, 0)
        self.player_hp = 100
        self.player_max_hp = 100
        self.player_attack = 15
        self.player_defense = 5
        self.inventory: List[Dict] = []
        self.gold = 0
        self.xp = 0
        self.floor = 1
        self.game_over = False
        self.won = False
        
        self._generate_dungeon()
    
    def _generate_dungeon(self):
        """Generate dungeon layout"""
        self.grid = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                room_type = self._determine_room_type(x, y)
                room = DungeonRoom(x, y, room_type)
                
                # Add contents based on room type
                if room_type == "monster":
                    room.contents["monster"] = random.choice(list(self.MONSTERS.keys()))
                elif room_type == "treasure":
                    room.contents["item"] = random.choice(self.TREASURE_ITEMS).copy()
                    room.contents["gold"] = random.randint(10, 50)
                elif room_type == "trap":
                    room.contents["damage"] = random.randint(10, 25)
                elif room_type == "boss":
                    room.contents["monster"] = "dragon"
                
                row.append(room)
            self.grid.append(row)
        
        # Set entrance and exit
        self.grid[0][0].room_type = "entrance"
        self.grid[self.size-1][self.size-1].room_type = "exit"
        self.player_pos = (0, 0)
        self.grid[0][0].visited = True
    
    def _determine_room_type(self, x: int, y: int) -> str:
        """Determine room type based on position and randomness"""
        if (x, y) == (0, 0) or (x, y) == (self.size-1, self.size-1):
            return "empty"
        
        rand = random.random()
        if rand < 0.3:
            return "monster"
        elif rand < 0.5:
            return "treasure"
        elif rand < 0.6:
            return "trap"
        elif rand < 0.65 and (x, y) == (self.size-2, self.size-2):
            return "boss"
        else:
            return "empty"
    
    def move(self, direction: str) -> Dict:
        """Move player in a direction"""
        x, y = self.player_pos
        
        if direction == "up" and y > 0:
            y -= 1
        elif direction == "down" and y < self.size - 1:
            y += 1
        elif direction == "left" and x > 0:
            x -= 1
        elif direction == "right" and x < self.size - 1:
            x += 1
        else:
            return {"success": False, "message": "Can't move that way!"}
        
        self.player_pos = (x, y)
        room = self.grid[y][x]
        room.visited = True
        
        result = {"success": True, "room": room.room_type, "events": []}
        
        # Handle room events
        if room.room_type == "monster" and "monster" in room.contents:
            monster_key = room.contents["monster"]
            monster = self.MONSTERS[monster_key]
            result["events"].append({"type": "encounter", "monster": monster})
        elif room.room_type == "treasure":
            if "item" in room.contents:
                self.inventory.append(room.contents["item"])
                result["events"].append({"type": "treasure", "item": room.contents["item"]})
            if "gold" in room.contents:
                self.gold += room.contents["gold"]
                result["events"].append({"type": "gold", "amount": room.contents["gold"]})
            room.room_type = "empty"  # Clear treasure
        elif room.room_type == "trap":
            damage = room.contents.get("damage", 15)
            self.player_hp -= damage
            result["events"].append({"type": "trap", "damage": damage})
            room.room_type = "empty"  # Disarm trap
            if self.player_hp <= 0:
                self.game_over = True
                result["game_over"] = True
        elif room.room_type == "exit":
            self.won = True
            self.game_over = True
            result["events"].append({"type": "exit", "message": "You found the exit!"})
        
        return result
    
    def fight(self, action: str = "attack") -> Dict:
        """Handle combat"""
        x, y = self.player_pos
        room = self.grid[y][x]
        
        if room.room_type != "monster" and room.room_type != "boss":
            return {"success": False, "message": "No monster to fight!"}
        
        monster_key = room.contents.get("monster", "goblin")
        monster = self.MONSTERS[monster_key]
        
        result = {"success": True, "combat_log": []}
        
        # Player attacks
        player_damage = max(1, self.player_attack - monster.defense)
        player_damage = random.randint(int(player_damage * 0.8), int(player_damage * 1.2))
        monster.hp -= player_damage
        result["combat_log"].append(f"You hit {monster.name} for {player_damage} damage!")
        
        if monster.hp <= 0:
            # Monster defeated
            self.xp += monster.xp_reward
            self.gold += monster.gold_reward
            result["combat_log"].append(f"You defeated {monster.name}!")
            result["combat_log"].append(f"Gained {monster.xp_reward} XP and {monster.gold_reward} gold!")
            result["victory"] = True
            room.room_type = "empty"
            del room.contents["monster"]
            return result
        
        # Monster attacks
        monster_damage = max(1, monster.attack - self.player_defense)
        monster_damage = random.randint(int(monster_damage * 0.8), int(monster_damage * 1.2))
        self.player_hp -= monster_damage
        result["combat_log"].append(f"{monster.name} hits you for {monster_damage} damage!")
        
        if self.player_hp <= 0:
            self.game_over = True
            result["game_over"] = True
            result["combat_log"].append("You have been defeated!")
        
        result["monster_hp"] = monster.hp
        result["player_hp"] = self.player_hp
        
        return result
    
    def use_item(self, item_index: int) -> Dict:
        """Use an item from inventory"""
        if item_index >= len(self.inventory):
            return {"success": False, "message": "Invalid item!"}
        
        item = self.inventory[item_index]
        
        if item["type"] == "consumable":
            if item["effect"] == "heal":
                heal_amount = item["value"]
                old_hp = self.player_hp
                self.player_hp = min(self.player_max_hp, self.player_hp + heal_amount)
                actual_heal = self.player_hp - old_hp
                del self.inventory[item_index]
                return {"success": True, "message": f"Healed for {actual_heal} HP!"}
        
        return {"success": False, "message": "Can't use this item now!"}
    
    def get_map_visual(self) -> str:
        """Get dungeon map visual"""
        icons = {
            "entrance": "🚪", "exit": "🌟", "empty": "⬜",
            "monster": "👹", "treasure": "💎", "trap": "💀",
            "boss": "🐉", "unknown": "⬛"
        }
        
        visual = "╔════════════════════════════════════╗\n║         🏰 DUNGEON MAP             ║\n╠════════════════════════════════════╣\n║                                    ║\n"
        
        for y in range(self.size):
            row = "║   "
            for x in range(self.size):
                if (x, y) == self.player_pos:
                    row += "🧙 "
                elif self.grid[y][x].visited:
                    row += f"{icons.get(self.grid[y][x].room_type, '⬜')} "
                else:
                    row += f"{icons['unknown']} "
            row += "  ║\n"
            visual += row
        
        visual += "║                                    ║\n"
        visual += f"║ HP: {self.player_hp}/{self.player_max_hp}  Gold: {self.gold}  XP: {self.xp}  ║\n"
        visual += "╚════════════════════════════════════╝"
        
        return visual

# Active dungeon storage
active_dungeons = {}

def create_dungeon(user_id: int, size: int = 5) -> str:
    """Create a new dungeon for user"""
    dungeon_id = f"dungeon_{user_id}_{random.randint(1000, 9999)}"
    dungeon = DungeonCrawler(user_id, size)
    active_dungeons[dungeon_id] = dungeon
    return dungeon_id

def get_dungeon(dungeon_id: str) -> Optional[DungeonCrawler]:
    """Get active dungeon"""
    return active_dungeons.get(dungeon_id)

def end_dungeon(dungeon_id: str):
    """End a dungeon run"""
    if dungeon_id in active_dungeons:
        del active_dungeons[dungeon_id]
