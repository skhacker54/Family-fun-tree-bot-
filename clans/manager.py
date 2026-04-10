"""
Clan/Guild Manager for Fam Tree Bot
====================================
Manage clans, clan wars, and alliances
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class ClanMember:
    """Clan member data"""
    user_id: int
    username: str
    role: str = "member"  # leader, officer, member
    joined_at: datetime = field(default_factory=datetime.utcnow)
    contribution: int = 0

@dataclass
class Clan:
    """Clan data"""
    id: str
    name: str
    tag: str
    description: str
    leader_id: int
    created_at: datetime = field(default_factory=datetime.utcnow)
    members: List[ClanMember] = field(default_factory=list)
    bank: int = 0
    level: int = 1
    xp: int = 0
    wars_won: int = 0
    wars_lost: int = 0
    territory: List[str] = field(default_factory=list)

class ClanManager:
    """Manage clans and clan operations"""
    
    CLAN_LEVELS = {
        1: {"max_members": 10, "bonus": 0},
        2: {"max_members": 20, "bonus": 5},
        3: {"max_members": 30, "bonus": 10},
        4: {"max_members": 50, "bonus": 15},
        5: {"max_members": 100, "bonus": 25},
    }
    
    def __init__(self):
        self.clans: Dict[str, Clan] = {}
        self.user_clan: Dict[int, str] = {}  # user_id -> clan_id
        self.pending_invites: Dict[int, List[str]] = {}  # user_id -> [clan_ids]
    
    def create_clan(self, name: str, tag: str, description: str, leader_id: int, leader_name: str) -> Optional[Clan]:
        """Create a new clan"""
        # Check if user already in clan
        if leader_id in self.user_clan:
            return None
        
        # Check tag availability
        for clan in self.clans.values():
            if clan.tag.lower() == tag.lower():
                return None
        
        clan_id = f"clan_{leader_id}_{random.randint(1000, 9999)}"
        
        clan = Clan(
            id=clan_id,
            name=name,
            tag=tag,
            description=description,
            leader_id=leader_id
        )
        
        # Add leader as first member
        leader = ClanMember(user_id=leader_id, username=leader_name, role="leader")
        clan.members.append(leader)
        
        self.clans[clan_id] = clan
        self.user_clan[leader_id] = clan_id
        
        return clan
    
    def disband_clan(self, clan_id: str, user_id: int) -> bool:
        """Disband a clan"""
        clan = self.clans.get(clan_id)
        if not clan or clan.leader_id != user_id:
            return False
        
        # Remove all members
        for member in clan.members:
            if member.user_id in self.user_clan:
                del self.user_clan[member.user_id]
        
        del self.clans[clan_id]
        return True
    
    def invite_member(self, clan_id: str, user_id: int, target_id: int) -> bool:
        """Invite a user to clan"""
        clan = self.clans.get(clan_id)
        if not clan:
            return False
        
        # Check if inviter is officer or leader
        inviter = next((m for m in clan.members if m.user_id == user_id), None)
        if not inviter or inviter.role not in ["leader", "officer"]:
            return False
        
        # Check clan capacity
        max_members = self.CLAN_LEVELS.get(clan.level, {}).get("max_members", 10)
        if len(clan.members) >= max_members:
            return False
        
        # Add to pending invites
        if target_id not in self.pending_invites:
            self.pending_invites[target_id] = []
        
        if clan_id not in self.pending_invites[target_id]:
            self.pending_invites[target_id].append(clan_id)
        
        return True
    
    def accept_invite(self, user_id: int, username: str, clan_id: str) -> bool:
        """Accept clan invite"""
        if user_id in self.user_clan:
            return False  # Already in clan
        
        if user_id not in self.pending_invites or clan_id not in self.pending_invites[user_id]:
            return False  # No invite
        
        clan = self.clans.get(clan_id)
        if not clan:
            return False
        
        # Check capacity
        max_members = self.CLAN_LEVELS.get(clan.level, {}).get("max_members", 10)
        if len(clan.members) >= max_members:
            return False
        
        # Add member
        member = ClanMember(user_id=user_id, username=username, role="member")
        clan.members.append(member)
        self.user_clan[user_id] = clan_id
        
        # Remove invite
        self.pending_invites[user_id].remove(clan_id)
        if not self.pending_invites[user_id]:
            del self.pending_invites[user_id]
        
        return True
    
    def kick_member(self, clan_id: str, user_id: int, target_id: int) -> bool:
        """Kick a member from clan"""
        clan = self.clans.get(clan_id)
        if not clan:
            return False
        
        # Check if kicker has permission
        kicker = next((m for m in clan.members if m.user_id == user_id), None)
        if not kicker or kicker.role not in ["leader", "officer"]:
            return False
        
        # Can't kick leader
        target = next((m for m in clan.members if m.user_id == target_id), None)
        if not target or target.role == "leader":
            return False
        
        # Remove member
        clan.members.remove(target)
        if target_id in self.user_clan:
            del self.user_clan[target_id]
        
        return True
    
    def promote_member(self, clan_id: str, user_id: int, target_id: int) -> bool:
        """Promote a member"""
        clan = self.clans.get(clan_id)
        if not clan or clan.leader_id != user_id:
            return False
        
        target = next((m for m in clan.members if m.user_id == target_id), None)
        if not target:
            return False
        
        if target.role == "member":
            target.role = "officer"
        elif target.role == "officer":
            target.role = "leader"
            # Transfer leadership
            old_leader = next((m for m in clan.members if m.role == "leader"), None)
            if old_leader:
                old_leader.role = "officer"
            clan.leader_id = target_id
        
        return True
    
    def donate(self, clan_id: str, user_id: int, amount: int) -> bool:
        """Donate to clan bank"""
        clan = self.clans.get(clan_id)
        if not clan:
            return False
        
        member = next((m for m in clan.members if m.user_id == user_id), None)
        if not member:
            return False
        
        clan.bank += amount
        member.contribution += amount
        
        # Add XP based on donation
        clan.xp += amount // 100
        self._check_level_up(clan)
        
        return True
    
    def _check_level_up(self, clan: Clan):
        """Check if clan should level up"""
        xp_needed = clan.level * 1000
        while clan.xp >= xp_needed:
            clan.xp -= xp_needed
            clan.level += 1
            xp_needed = clan.level * 1000
    
    def get_clan_visual(self, clan_id: str) -> str:
        """Get visual clan info"""
        clan = self.clans.get(clan_id)
        if not clan:
            return "Clan not found!"
        
        max_members = self.CLAN_LEVELS.get(clan.level, {}).get("max_members", 10)
        bonus = self.CLAN_LEVELS.get(clan.level, {}).get("bonus", 0)
        
        visual = f"""
╔══════════════════════════════════════════════════════════════╗
║                    ⚔️ {clan.name[:20]:^20} ⚔️                    ║
║                    [{clan.tag}] Level {clan.level}                          ║
╠══════════════════════════════════════════════════════════════╣
║  {clan.description[:50]:<50} ║
║                                                              ║
║  💰 Bank: ${clan.bank:,}                                    ║
║  ⭐ XP: {clan.xp}/{clan.level * 1000}                                    ║
║  👥 Members: {len(clan.members)}/{max_members}                                    ║
║  🎁 Bonus: +{bonus}% income                                  ║
║                                                              ║
║  🏆 Wars: {clan.wars_won}W/{clan.wars_lost}L                                    ║
╠══════════════════════════════════════════════════════════════╣
║  MEMBERS:                                                    ║
"""
        for member in clan.members[:10]:  # Show first 10
            role_icon = {"leader": "👑", "officer": "⭐", "member": "👤"}.get(member.role, "👤")
            visual += f"║  {role_icon} {member.username[:15]:<15} (${member.contribution:,})              ║\n"
        
        visual += "╚══════════════════════════════════════════════════════════════╝"
        
        return visual
    
    def get_leaderboard(self) -> List[Clan]:
        """Get clans sorted by level and bank"""
        return sorted(
            self.clans.values(),
            key=lambda c: (c.level, c.bank),
            reverse=True
        )[:10]

# Global clan manager
clan_manager = ClanManager()
