"""
Database Models for Fam Tree Bot
================================
SQLAlchemy models for all bot entities
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, BigInteger, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, timedelta
import json
from config.settings import DATABASE_URL

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    language_code = Column(String(10), default='en')
    
    # Economy
    balance = Column(Float, default=1000.0)
    bank_balance = Column(Float, default=0.0)
    reputation = Column(Integer, default=0)
    
    # Profile
    profile_pic = Column(Text, default=None)
    customizations = Column(JSON, default=dict)
    
    # Combat
    current_weapon = Column(String(50), default='punch')
    health = Column(Integer, default=5)
    max_health = Column(Integer, default=5)
    is_dead = Column(Boolean, default=False)
    death_time = Column(DateTime, default=None)
    
    # Daily
    last_daily = Column(DateTime, default=None)
    daily_streak = Column(Integer, default=0)
    gemstone = Column(String(20), default=None)
    
    # Job
    job = Column(String(50), default='unemployed')
    
    # Factory
    factory_rating = Column(Integer, default=0)
    
    # Garden
    garden_slots = Column(Integer, default=9)
    barn_size = Column(Integer, default=500)
    
    # Limits tracking
    robbery_count_today = Column(Integer, default=0)
    kill_count_today = Column(Integer, default=0)
    last_reset_day = Column(DateTime, default=datetime.utcnow)
    
    # Settings
    settings = Column(JSON, default=dict)
    
    # Stats
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # Referral
    referral_code = Column(String(20), unique=True)
    referred_by = Column(BigInteger, default=None)
    referral_count = Column(Integer, default=0)
    
    # Relationships
    family_members = relationship("FamilyMember", back_populates="user", foreign_keys="FamilyMember.user_id")
    children = relationship("FamilyMember", back_populates="parent", foreign_keys="FamilyMember.parent_id")
    partners = relationship("Partnership", back_populates="user1", foreign_keys="Partnership.user1_id")
    friends_sent = relationship("Friendship", back_populates="user1", foreign_keys="Friendship.user1_id")
    friends_received = relationship("Friendship", back_populates="user2", foreign_keys="Friendship.user2_id")
    workers = relationship("Worker", back_populates="owner", foreign_keys="Worker.owner_id")
    employed_as = relationship("Worker", back_populates="worker", foreign_keys="Worker.worker_id")
    garden_plots = relationship("GardenPlot", back_populates="owner")
    barn_items = relationship("BarnItem", back_populates="owner")
    insurance_policies = relationship("Insurance", back_populates="owner")
    achievements = relationship("Achievement", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"

class FamilyMember(Base):
    __tablename__ = 'family_members'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    parent_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    relationship_type = Column(String(20), default='adopted')  # adopted, biological, sibling
    adopted_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="family_members", foreign_keys=[user_id])
    parent = relationship("User", back_populates="children", foreign_keys=[parent_id])

class Partnership(Base):
    __tablename__ = 'partnerships'
    
    id = Column(Integer, primary_key=True)
    user1_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    user2_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    married_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    user1 = relationship("User", back_populates="partners", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])

class Friendship(Base):
    __tablename__ = 'friendships'
    
    id = Column(Integer, primary_key=True)
    user1_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    user2_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    status = Column(String(20), default='pending')  # pending, accepted, blocked
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user1 = relationship("User", back_populates="friends_sent", foreign_keys=[user1_id])
    user2 = relationship("User", back_populates="friends_received", foreign_keys=[user2_id])

class Worker(Base):
    __tablename__ = 'workers'
    
    id = Column(Integer, primary_key=True)
    owner_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    worker_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    price = Column(Float, default=0.0)
    rating = Column(Integer, default=0)
    status = Column(String(20), default='idle')  # idle, working, completed
    work_start_time = Column(DateTime, default=None)
    work_end_time = Column(DateTime, default=None)
    has_shield = Column(Boolean, default=False)
    shield_expires = Column(DateTime, default=None)
    hired_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="workers", foreign_keys=[owner_id])
    worker = relationship("User", back_populates="employed_as", foreign_keys=[worker_id])

class GardenPlot(Base):
    __tablename__ = 'garden_plots'
    
    id = Column(Integer, primary_key=True)
    owner_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    plot_number = Column(Integer)
    crop_type = Column(String(50), default=None)
    planted_at = Column(DateTime, default=None)
    growth_time = Column(Integer, default=0)  # in seconds
    is_ready = Column(Boolean, default=False)
    is_empty = Column(Boolean, default=True)
    fertilized = Column(Boolean, default=False)
    
    owner = relationship("User", back_populates="garden_plots")

class BarnItem(Base):
    __tablename__ = 'barn_items'
    
    id = Column(Integer, primary_key=True)
    owner_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    item_type = Column(String(50))  # crop, recipe, product
    item_name = Column(String(50))
    quantity = Column(Integer, default=0)
    
    owner = relationship("User", back_populates="barn_items")

class Insurance(Base):
    __tablename__ = 'insurance'
    
    id = Column(Integer, primary_key=True)
    owner_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    insured_user_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    insurance_type = Column(String(20))  # close_family, family, friend
    payout_multiplier = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    owner = relationship("User", back_populates="insurance_policies")

class MarketListing(Base):
    __tablename__ = 'market_listings'
    
    id = Column(Integer, primary_key=True)
    seller_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    crop_type = Column(String(50))
    quantity = Column(Integer)
    price_per_unit = Column(Float)
    listed_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class CookingSession(Base):
    __tablename__ = 'cooking_sessions'
    
    id = Column(Integer, primary_key=True)
    creator_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    recipe_name = Column(String(50))
    participants = Column(JSON, default=list)
    ingredients_contributed = Column(JSON, default=dict)
    started_at = Column(DateTime, default=datetime.utcnow)
    completes_at = Column(DateTime)
    is_complete = Column(Boolean, default=False)

class Achievement(Base):
    __tablename__ = 'achievements'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    achievement_type = Column(String(50))
    rarity = Column(String(20), default='bronze')  # bronze, silver, gold, diamond, platinum
    unlocked_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="achievements")

class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    notification_type = Column(String(50))
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="notifications")

class GameSession(Base):
    __tablename__ = 'game_sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    game_type = Column(String(50))
    bet_amount = Column(Float, default=0.0)
    current_multiplier = Column(Float, default=1.0)
    status = Column(String(20), default='active')  # active, won, lost
    started_at = Column(DateTime, default=datetime.utcnow)
    data = Column(JSON, default=dict)

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    from_user_id = Column(BigInteger, ForeignKey('users.telegram_id'), nullable=True)
    to_user_id = Column(BigInteger, ForeignKey('users.telegram_id'), nullable=True)
    amount = Column(Float)
    transaction_type = Column(String(50))  # transfer, rob, kill, daily, work, etc.
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class BlockedUser(Base):
    __tablename__ = 'blocked_users'
    
    id = Column(Integer, primary_key=True)
    blocker_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    blocked_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    blocked_at = Column(DateTime, default=datetime.utcnow)

class CustomGIF(Base):
    __tablename__ = 'custom_gifs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    gif_type = Column(String(50))  # robyes, robno, killyes, killno
    file_id = Column(String(200))
    added_at = Column(DateTime, default=datetime.utcnow)

class Clan(Base):
    __tablename__ = 'clans'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    tag = Column(String(10))
    leader_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    bank_balance = Column(Float, default=0.0)
    
class ClanMember(Base):
    __tablename__ = 'clan_members'
    
    id = Column(Integer, primary_key=True)
    clan_id = Column(Integer, ForeignKey('clans.id'))
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    role = Column(String(20), default='member')  # leader, officer, member
    joined_at = Column(DateTime, default=datetime.utcnow)

# Database initialization
def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
