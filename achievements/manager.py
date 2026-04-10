"""
Achievement Manager for Fam Tree Bot
=====================================
Track and award achievements
"""

from datetime import datetime
from typing import Dict, List, Optional

class AchievementManager:
    """Manage user achievements"""
    
    ACHIEVEMENTS = {
        # Family achievements
        "first_adoption": {
            "name": "First Steps",
            "description": "Adopt your first child",
            "category": "family",
            "rarity": "bronze",
            "reward": {"money": 100, "xp": 50}
        },
        "big_family": {
            "name": "Big Family",
            "description": "Have 5 children",
            "category": "family",
            "rarity": "silver",
            "reward": {"money": 500, "xp": 200}
        },
        "royal_family": {
            "name": "Royal Family",
            "description": "Have 8 children (max)",
            "category": "family",
            "rarity": "gold",
            "reward": {"money": 2000, "xp": 500, "badge": "Royal"}
        },
        "first_marriage": {
            "name": "Just Married",
            "description": "Get married for the first time",
            "category": "family",
            "rarity": "bronze",
            "reward": {"money": 200, "xp": 100}
        },
        "polygamist": {
            "name": "Polygamist",
            "description": "Have 3 partners",
            "category": "family",
            "rarity": "silver",
            "reward": {"money": 1000, "xp": 300}
        },
        
        # Economy achievements
        "first_1000": {
            "name": "First Thousand",
            "description": "Earn $1,000",
            "category": "wealth",
            "rarity": "bronze",
            "reward": {"money": 100, "xp": 50}
        },
        "first_10000": {
            "name": "Ten Thousand",
            "description": "Earn $10,000",
            "category": "wealth",
            "rarity": "silver",
            "reward": {"money": 1000, "xp": 200}
        },
        "millionaire": {
            "name": "Millionaire",
            "description": "Earn $1,000,000",
            "category": "wealth",
            "rarity": "gold",
            "reward": {"money": 100000, "xp": 5000, "badge": "Millionaire"}
        },
        "banker": {
            "name": "Banker",
            "description": "Have $100,000 in bank",
            "category": "wealth",
            "rarity": "silver",
            "reward": {"money": 5000, "xp": 500}
        },
        
        # Combat achievements
        "first_blood": {
            "name": "First Blood",
            "description": "Win your first PvP battle",
            "category": "combat",
            "rarity": "bronze",
            "reward": {"money": 200, "xp": 100}
        },
        "serial_killer": {
            "name": "Serial Killer",
            "description": "Win 50 PvP battles",
            "category": "combat",
            "rarity": "silver",
            "reward": {"money": 5000, "xp": 1000}
        },
        "legendary_warrior": {
            "name": "Legendary Warrior",
            "description": "Win 100 PvP battles",
            "category": "combat",
            "rarity": "gold",
            "reward": {"money": 20000, "xp": 3000, "badge": "Warrior"}
        },
        "master_thief": {
            "name": "Master Thief",
            "description": "Successfully rob 100 times",
            "category": "combat",
            "rarity": "silver",
            "reward": {"money": 3000, "xp": 500}
        },
        
        # Garden achievements
        "green_thumb": {
            "name": "Green Thumb",
            "description": "Harvest 10 crops",
            "category": "garden",
            "rarity": "bronze",
            "reward": {"money": 100, "xp": 50}
        },
        "master_farmer": {
            "name": "Master Farmer",
            "description": "Harvest 100 crops",
            "category": "garden",
            "rarity": "silver",
            "reward": {"money": 1000, "xp": 300}
        },
        "agricultural_tycoon": {
            "name": "Agricultural Tycoon",
            "description": "Harvest 1000 crops",
            "category": "garden",
            "rarity": "gold",
            "reward": {"money": 10000, "xp": 1000, "badge": "Farmer"}
        },
        "max_garden": {
            "name": "Maxed Out",
            "description": "Expand garden to 12 slots",
            "category": "garden",
            "rarity": "silver",
            "reward": {"money": 2000, "xp": 400}
        },
        
        # Social achievements
        "popular": {
            "name": "Popular",
            "description": "Have 10 friends",
            "category": "social",
            "rarity": "bronze",
            "reward": {"money": 500, "xp": 100}
        },
        "socialite": {
            "name": "Socialite",
            "description": "Have 50 friends",
            "category": "social",
            "rarity": "silver",
            "reward": {"money": 3000, "xp": 500}
        },
        "celebrity": {
            "name": "Celebrity",
            "description": "Have 100 friends",
            "category": "social",
            "rarity": "gold",
            "reward": {"money": 10000, "xp": 1500, "badge": "Celebrity"}
        },
        
        # Game achievements
        "lucky": {
            "name": "Lucky",
            "description": "Win lottery once",
            "category": "games",
            "rarity": "bronze",
            "reward": {"money": 500, "xp": 100}
        },
        "gambler": {
            "name": "Gambler",
            "description": "Win $10,000 from games",
            "category": "games",
            "rarity": "silver",
            "reward": {"money": 2000, "xp": 300}
        },
        "dungeon_crawler": {
            "name": "Dungeon Crawler",
            "description": "Complete 5 dungeon runs",
            "category": "games",
            "rarity": "silver",
            "reward": {"money": 3000, "xp": 500}
        },
        
        # Special achievements
        "early_adopter": {
            "name": "Early Adopter",
            "description": "Join during beta",
            "category": "special",
            "rarity": "gold",
            "reward": {"money": 10000, "xp": 1000, "badge": "Founder"}
        },
        "dedicated": {
            "name": "Dedicated",
            "description": "Login for 30 days straight",
            "category": "special",
            "rarity": "silver",
            "reward": {"money": 5000, "xp": 500}
        },
        "veteran": {
            "name": "Veteran",
            "description": "Play for 1 year",
            "category": "special",
            "rarity": "gold",
            "reward": {"money": 50000, "xp": 5000, "badge": "Veteran"}
        },
    }
    
    RARITY_COLORS = {
        "bronze": "🥉",
        "silver": "🥈",
        "gold": "🥇",
        "platinum": "💎",
        "legendary": "👑"
    }
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.unlocked: List[str] = []
        self.progress: Dict[str, int] = {}
    
    def check_achievement(self, achievement_id: str, current_value: int) -> Optional[Dict]:
        """Check if achievement should be unlocked"""
        if achievement_id in self.unlocked:
            return None
        
        achievement = self.ACHIEVEMENTS.get(achievement_id)
        if not achievement:
            return None
        
        # Update progress
        self.progress[achievement_id] = current_value
        
        # Check if requirement met (simplified - actual requirements would be more complex)
        thresholds = {
            "first_adoption": 1, "big_family": 5, "royal_family": 8,
            "first_marriage": 1, "polygamist": 3,
            "first_1000": 1000, "first_10000": 10000, "millionaire": 1000000,
            "first_blood": 1, "serial_killer": 50, "legendary_warrior": 100,
            "green_thumb": 10, "master_farmer": 100, "agricultural_tycoon": 1000,
            "popular": 10, "socialite": 50, "celebrity": 100,
        }
        
        threshold = thresholds.get(achievement_id, 1)
        if current_value >= threshold:
            return self.unlock_achievement(achievement_id)
        
        return None
    
    def unlock_achievement(self, achievement_id: str) -> Dict:
        """Unlock an achievement"""
        if achievement_id not in self.unlocked:
            self.unlocked.append(achievement_id)
        
        achievement = self.ACHIEVEMENTS.get(achievement_id, {})
        return {
            "id": achievement_id,
            "name": achievement.get("name"),
            "description": achievement.get("description"),
            "rarity": achievement.get("rarity"),
            "reward": achievement.get("reward"),
            "unlocked_at": datetime.utcnow().isoformat()
        }
    
    def get_achievement_visual(self) -> str:
        """Get visual achievement list"""
        visual = "╔══════════════════════════════════════════════════════════════╗\n"
        visual += "║                    🏆 ACHIEVEMENTS                           ║\n╠══════════════════════════════════════════════════════════════╣\n"
        
        # Group by category
        by_category = {}
        for aid, achievement in self.ACHIEVEMENTS.items():
            cat = achievement["category"]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append((aid, achievement))
        
        for category, achievements in by_category.items():
            visual += f"║  📁 {category.upper()}                                           ║\n"
            for aid, achievement in achievements[:3]:  # Show first 3 per category
                unlocked = aid in self.unlocked
                status = "✅" if unlocked else "⬜"
                rarity = self.RARITY_COLORS.get(achievement["rarity"], "🥉")
                visual += f"║  {status} {rarity} {achievement['name'][:25]:<25}         ║\n"
            visual += "║                                                              ║\n"
        
        visual += f"║  📊 Progress: {len(self.unlocked)}/{len(self.ACHIEVEMENTS)} achievements unlocked          ║\n"
        visual += "╚══════════════════════════════════════════════════════════════╝"
        
        return visual

# Achievement managers
achievement_managers = {}

def get_achievement_manager(user_id: int) -> AchievementManager:
    """Get or create achievement manager for user"""
    if user_id not in achievement_managers:
        achievement_managers[user_id] = AchievementManager(user_id)
    return achievement_managers[user_id]
