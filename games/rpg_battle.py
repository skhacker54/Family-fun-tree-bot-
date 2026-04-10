"""
RPG Battle System for Fam Tree Bot
===================================
Advanced turn-based combat system
"""

import random
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class BattleStats:
    hp: int
    max_hp: int
    mp: int
    max_mp: int
    attack: int
    defense: int
    speed: int
    level: int
    xp: int

@dataclass
class BattleSkill:
    name: str
    damage: int
    mp_cost: int
    accuracy: int
    element: str

class RPGCharacter:
    """RPG Character class"""
    
    SKILLS = {
        "slash": BattleSkill("Slash", 25, 5, 90, "physical"),
        "fireball": BattleSkill("Fireball", 40, 15, 85, "fire"),
        "heal": BattleSkill("Heal", -30, 20, 100, "magic"),
        "thunder": BattleSkill("Thunder", 50, 25, 80, "lightning"),
        "ice_shard": BattleSkill("Ice Shard", 35, 12, 88, "ice"),
        "poison_strike": BattleSkill("Poison Strike", 20, 10, 75, "poison"),
    }
    
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name
        self.stats = BattleStats(
            hp=100, max_hp=100,
            mp=50, max_mp=50,
            attack=20, defense=15,
            speed=10, level=1, xp=0
        )
        self.skills = ["slash"]
        self.equipment = {"weapon": None, "armor": None, "accessory": None}
    
    def level_up(self):
        """Level up the character"""
        self.stats.level += 1
        self.stats.max_hp += 10
        self.stats.max_mp += 5
        self.stats.attack += 3
        self.stats.defense += 2
        self.stats.speed += 1
        self.stats.hp = self.stats.max_hp
        self.stats.mp = self.stats.max_mp
        
        # Learn new skills
        if self.stats.level == 3:
            self.skills.append("fireball")
        elif self.stats.level == 5:
            self.skills.append("heal")
        elif self.stats.level == 7:
            self.skills.append("thunder")
        elif self.stats.level == 10:
            self.skills.append("ice_shard")
    
    def use_skill(self, skill_name: str, target: 'RPGCharacter') -> Dict:
        """Use a skill on target"""
        if skill_name not in self.skills:
            return {"success": False, "message": "Skill not learned!"}
        
        skill = self.SKILLS.get(skill_name)
        if not skill:
            return {"success": False, "message": "Invalid skill!"}
        
        if self.stats.mp < skill.mp_cost:
            return {"success": False, "message": "Not enough MP!"}
        
        self.stats.mp -= skill.mp_cost
        
        # Check accuracy
        if random.randint(1, 100) > skill.accuracy:
            return {"success": True, "hit": False, "message": f"{self.name} missed!"}
        
        # Calculate damage
        if skill_name == "heal":
            heal_amount = abs(skill.damage)
            self.stats.hp = min(self.stats.max_hp, self.stats.hp + heal_amount)
            return {
                "success": True,
                "hit": True,
                "heal": heal_amount,
                "message": f"{self.name} healed for {heal_amount} HP!"
            }
        
        damage = skill.damage + self.stats.attack - target.stats.defense
        damage = max(1, damage)  # Minimum 1 damage
        damage = random.randint(int(damage * 0.8), int(damage * 1.2))  # Variance
        
        target.stats.hp = max(0, target.stats.hp - damage)
        
        return {
            "success": True,
            "hit": True,
            "damage": damage,
            "message": f"{self.name} used {skill.name} for {damage} damage!"
        }
    
    def basic_attack(self, target: 'RPGCharacter') -> Dict:
        """Basic attack"""
        damage = self.stats.attack - target.stats.defense
        damage = max(1, damage)
        damage = random.randint(int(damage * 0.9), int(damage * 1.1))
        
        target.stats.hp = max(0, target.stats.hp - damage)
        
        return {
            "success": True,
            "damage": damage,
            "message": f"{self.name} attacked for {damage} damage!"
        }
    
    def is_alive(self) -> bool:
        """Check if character is alive"""
        return self.stats.hp > 0
    
    def get_status_bar(self) -> str:
        """Get visual status bar"""
        hp_pct = self.stats.hp / self.stats.max_hp
        mp_pct = self.stats.mp / self.stats.max_mp
        
        hp_bar = '█' * int(hp_pct * 10) + '░' * (10 - int(hp_pct * 10))
        mp_bar = '█' * int(mp_pct * 10) + '░' * (10 - int(mp_pct * 10))
        
        return f"""
╔════════════════════════════════════╗
║ {self.name:^34} ║
║ Lv.{self.stats.level}                              ║
║ HP: [{hp_bar}] {self.stats.hp}/{self.stats.max_hp:<3}    ║
║ MP: [{mp_bar}] {self.stats.mp}/{self.stats.max_mp:<3}     ║
╚════════════════════════════════════╝"""

class BattleSystem:
    """Main battle system"""
    
    def __init__(self, player1: RPGCharacter, player2: RPGCharacter):
        self.player1 = player1
        self.player2 = player2
        self.turn = 0
        self.log = []
        self.active_player = player1 if player1.stats.speed >= player2.stats.speed else player2
    
    def execute_turn(self, action: str, skill_name: Optional[str] = None) -> Dict:
        """Execute a battle turn"""
        attacker = self.active_player
        defender = self.player2 if attacker == self.player1 else self.player1
        
        result = {"turn": self.turn, "actions": []}
        
        # Attacker's action
        if action == "attack":
            action_result = attacker.basic_attack(defender)
        elif action == "skill" and skill_name:
            action_result = attacker.use_skill(skill_name, defender)
        elif action == "defend":
            action_result = {
                "success": True,
                "message": f"{attacker.name} is defending!",
                "defending": True
            }
        else:
            action_result = {"success": False, "message": "Invalid action!"}
        
        result["actions"].append(action_result)
        self.log.append(action_result["message"])
        
        # Check win condition
        if not defender.is_alive():
            result["winner"] = attacker.user_id
            result["finished"] = True
            # Award XP
            xp_gain = random.randint(20, 50)
            attacker.stats.xp += xp_gain
            if attacker.stats.xp >= attacker.stats.level * 100:
                attacker.level_up()
                result["level_up"] = True
            return result
        
        # Switch turns
        self.active_player = defender
        self.turn += 1
        
        result["finished"] = False
        return result
    
    def get_battle_visual(self) -> str:
        """Get visual battle representation"""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║                    ⚔️ BATTLE ARENA                           ║
╠══════════════════════════════════════════════════════════════╣
{self.player1.get_status_bar()}
║                                                              ║
║                          VS                                  ║
║                                                              ║
{self.player2.get_status_bar()}
╚══════════════════════════════════════════════════════════════╝
"""

# Active battles storage
active_battles = {}

def start_battle(user1_id: int, user1_name: str, user2_id: int, user2_name: str) -> str:
    """Start a new battle"""
    battle_id = f"{user1_id}_{user2_id}_{random.randint(1000, 9999)}"
    
    player1 = RPGCharacter(user1_id, user1_name)
    player2 = RPGCharacter(user2_id, user2_name)
    
    battle = BattleSystem(player1, player2)
    active_battles[battle_id] = battle
    
    return battle_id

def get_battle(battle_id: str) -> Optional[BattleSystem]:
    """Get active battle"""
    return active_battles.get(battle_id)

def end_battle(battle_id: str):
    """End a battle"""
    if battle_id in active_battles:
        del active_battles[battle_id]
