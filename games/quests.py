"""
Quest System for Fam Tree Bot
==============================
Daily, weekly, and achievement quests
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Quest:
    """Quest data class"""
    id: str
    title: str
    description: str
    quest_type: str  # daily, weekly, story, achievement
    requirements: Dict
    rewards: Dict
    completed: bool = False
    progress: int = 0
    expires_at: Optional[datetime] = None

class QuestSystem:
    """Main quest system"""
    
    DAILY_QUESTS = [
        {
            "title": "Daily Harvest",
            "description": "Harvest 5 crops from your garden",
            "requirements": {"type": "harvest", "amount": 5},
            "rewards": {"money": 100, "xp": 20}
        },
        {
            "title": "Social Butterfly",
            "description": "Make 2 new friends",
            "requirements": {"type": "friend", "amount": 2},
            "rewards": {"money": 200, "xp": 30}
        },
        {
            "title": "Family Builder",
            "description": "Adopt 1 child",
            "requirements": {"type": "adopt", "amount": 1},
            "rewards": {"money": 300, "xp": 40}
        },
        {
            "title": "Market Trader",
            "description": "Sell 3 items at the market",
            "requirements": {"type": "sell", "amount": 3},
            "rewards": {"money": 150, "xp": 25}
        },
        {
            "title": "Warrior",
            "description": "Win 2 PvP battles",
            "requirements": {"type": "pvp_win", "amount": 2},
            "rewards": {"money": 250, "xp": 35}
        },
    ]
    
    WEEKLY_QUESTS = [
        {
            "title": "Master Farmer",
            "description": "Harvest 50 crops this week",
            "requirements": {"type": "harvest", "amount": 50},
            "rewards": {"money": 1000, "xp": 100, "item": "Golden Hoe"}
        },
        {
            "title": "Rich Trader",
            "description": "Earn $5000 from trading",
            "requirements": {"type": "trade_earn", "amount": 5000},
            "rewards": {"money": 500, "xp": 80, "item": "Merchant Badge"}
        },
        {
            "title": "Family Legend",
            "description": "Have 5 family members",
            "requirements": {"type": "family_size", "amount": 5},
            "rewards": {"money": 2000, "xp": 150, "item": "Family Crest"}
        },
    ]
    
    ACHIEVEMENT_QUESTS = [
        {
            "id": "first_blood",
            "title": "First Blood",
            "description": "Win your first PvP battle",
            "requirements": {"type": "pvp_win", "amount": 1},
            "rewards": {"money": 500, "xp": 50, "badge": "Warrior"}
        },
        {
            "id": "millionaire",
            "title": "Millionaire",
            "description": "Have $1,000,000 total wealth",
            "requirements": {"type": "wealth", "amount": 1000000},
            "rewards": {"money": 100000, "xp": 500, "badge": "Wealthy"}
        },
        {
            "id": "collector",
            "title": "Collector",
            "description": "Collect 100 different items",
            "requirements": {"type": "collect", "amount": 100},
            "rewards": {"money": 5000, "xp": 200, "badge": "Collector"}
        },
        {
            "id": "social_king",
            "title": "Social King",
            "description": "Have 50 friends",
            "requirements": {"type": "friends", "amount": 50},
            "rewards": {"money": 10000, "xp": 300, "badge": "Socialite"}
        },
        {
            "id": "dungeon_master",
            "title": "Dungeon Master",
            "description": "Complete 10 dungeon runs",
            "requirements": {"type": "dungeon_complete", "amount": 10},
            "rewards": {"money": 50000, "xp": 1000, "badge": "Explorer"}
        },
    ]
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.daily_quests: List[Quest] = []
        self.weekly_quests: List[Quest] = []
        self.achievements: List[Quest] = []
        self.last_daily_reset = None
        self.last_weekly_reset = None
        
        self._generate_daily_quests()
        self._generate_weekly_quests()
        self._load_achievements()
    
    def _generate_daily_quests(self):
        """Generate daily quests"""
        self.daily_quests = []
        selected = random.sample(self.DAILY_QUESTS, min(3, len(self.DAILY_QUESTS)))
        
        for i, quest_data in enumerate(selected):
            quest = Quest(
                id=f"daily_{i}",
                title=quest_data["title"],
                description=quest_data["description"],
                quest_type="daily",
                requirements=quest_data["requirements"],
                rewards=quest_data["rewards"],
                expires_at=datetime.utcnow() + timedelta(days=1)
            )
            self.daily_quests.append(quest)
        
        self.last_daily_reset = datetime.utcnow()
    
    def _generate_weekly_quests(self):
        """Generate weekly quests"""
        self.weekly_quests = []
        selected = random.sample(self.WEEKLY_QUESTS, min(2, len(self.WEEKLY_QUESTS)))
        
        for i, quest_data in enumerate(selected):
            quest = Quest(
                id=f"weekly_{i}",
                title=quest_data["title"],
                description=quest_data["description"],
                quest_type="weekly",
                requirements=quest_data["requirements"],
                rewards=quest_data["rewards"],
                expires_at=datetime.utcnow() + timedelta(weeks=1)
            )
            self.weekly_quests.append(quest)
        
        self.last_weekly_reset = datetime.utcnow()
    
    def _load_achievements(self):
        """Load achievement quests"""
        self.achievements = []
        
        for quest_data in self.ACHIEVEMENT_QUESTS:
            quest = Quest(
                id=quest_data["id"],
                title=quest_data["title"],
                description=quest_data["description"],
                quest_type="achievement",
                requirements=quest_data["requirements"],
                rewards=quest_data["rewards"]
            )
            self.achievements.append(quest)
    
    def update_progress(self, action_type: str, amount: int = 1) -> List[Quest]:
        """Update quest progress"""
        completed_quests = []
        
        # Update daily quests
        for quest in self.daily_quests:
            if not quest.completed and quest.requirements["type"] == action_type:
                quest.progress += amount
                if quest.progress >= quest.requirements["amount"]:
                    quest.completed = True
                    completed_quests.append(quest)
        
        # Update weekly quests
        for quest in self.weekly_quests:
            if not quest.completed and quest.requirements["type"] == action_type:
                quest.progress += amount
                if quest.progress >= quest.requirements["amount"]:
                    quest.completed = True
                    completed_quests.append(quest)
        
        # Update achievements
        for quest in self.achievements:
            if not quest.completed and quest.requirements["type"] == action_type:
                quest.progress += amount
                if quest.progress >= quest.requirements["amount"]:
                    quest.completed = True
                    completed_quests.append(quest)
        
        return completed_quests
    
    def check_expired(self):
        """Check and reset expired quests"""
        now = datetime.utcnow()
        
        # Check daily reset
        if self.last_daily_reset and (now - self.last_daily_reset).days >= 1:
            self._generate_daily_quests()
        
        # Check weekly reset
        if self.last_weekly_reset and (now - self.last_weekly_reset).days >= 7:
            self._generate_weekly_quests()
    
    def get_quest_visual(self) -> str:
        """Get visual quest list"""
        visual = "╔══════════════════════════════════════════════════════════════╗\n"
        visual += "║                    📜 QUEST JOURNAL                          ║\n╠══════════════════════════════════════════════════════════════╣\n"
        
        # Daily quests
        visual += "║  📅 DAILY QUESTS                                             ║\n"
        for quest in self.daily_quests:
            status = "✅" if quest.completed else "⬜"
            progress_pct = min(100, int((quest.progress / quest.requirements["amount"]) * 100))
            bar = "█" * (progress_pct // 10) + "░" * (10 - progress_pct // 10)
            visual += f"║  {status} {quest.title[:25]:<25} [{bar}] {progress_pct}%  ║\n"
        
        visual += "║                                                              ║\n"
        
        # Weekly quests
        visual += "║  📆 WEEKLY QUESTS                                            ║\n"
        for quest in self.weekly_quests:
            status = "✅" if quest.completed else "⬜"
            progress_pct = min(100, int((quest.progress / quest.requirements["amount"]) * 100))
            bar = "█" * (progress_pct // 10) + "░" * (10 - progress_pct // 10)
            visual += f"║  {status} {quest.title[:25]:<25} [{bar}] {progress_pct}%  ║\n"
        
        visual += "║                                                              ║\n"
        
        # Achievements
        visual += "║  🏆 ACHIEVEMENTS                                             ║\n"
        for quest in self.achievements[:5]:  # Show first 5
            status = "✅" if quest.completed else "⬜"
            visual += f"║  {status} {quest.title[:30]:<30}           ║\n"
        
        visual += "╚══════════════════════════════════════════════════════════════╝"
        
        return visual

# Active quest systems
quest_systems = {}

def get_quest_system(user_id: int) -> QuestSystem:
    """Get or create quest system for user"""
    if user_id not in quest_systems:
        quest_systems[user_id] = QuestSystem(user_id)
    else:
        quest_systems[user_id].check_expired()
    
    return quest_systems[user_id]
