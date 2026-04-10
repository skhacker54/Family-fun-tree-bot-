"""
Fam Tree Bot - Configuration Settings
======================================
Ultimate Telegram Family Simulation RPG Bot
"""

import os
from typing import Dict, List

# Try to load .env file if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # .env file support is optional

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
BOT_NAME = "@fam_tree_bot"
BOT_NAME_BETA = "@famtreebbot"
BOT_VERSION = "2.0.0"

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///fam_tree_bot.db")

# Performance Settings
RESPONSE_TIME_TARGET = 1.0  # seconds
MAX_CONCURRENT_USERS = 100000

# System Limits (EXACT - NO CHANGES)
LIMITS = {
    "max_friends": 100,
    "max_partners": 7,
    "max_children": 8,
    "max_robbery_per_day": 8,
    "max_kills_per_day": 5,
    "max_workers": 5,
    "garden_slots_start": 9,
    "garden_slots_max": 12,
    "barn_size": 500,
    "max_insurance": 10,
}

# Economy Settings
STARTING_BALANCE = 1000
DAILY_BASE_SALARY = 100
FRIEND_BONUS = 3000

# Weapon Arsenal (EXACT PRICES AND STATS)
WEAPONS = {
    "punch": {"price": 0, "rob_power": 50, "kill_power": 50},
    "blade": {"price": 100, "rob_power": 80, "kill_power": 100},
    "sword": {"price": 200, "rob_power": 100, "kill_power": 150},
    "pistol": {"price": 400, "rob_power": 160, "kill_power": 200},
    "gun": {"price": 500, "rob_power": 200, "kill_power": 200},
    "bow": {"price": 5000, "rob_power": 300, "kill_power": 100},
    "poison": {"price": 8000, "rob_power": 400, "kill_power": 200},
    "rocket_launcher": {"price": 10000, "rob_power": 500, "kill_power": 200},
}

# Jobs System
JOBS = {
    "unemployed": {"salary": 0, "benefit": None},
    "banker": {"salary": 100, "benefit": None},
    "policeman": {"salary": 100, "benefit": "higher_thief_protection"},
    "doctor": {"salary": 300, "benefit": "revive_1_heart_daily"},
    "scientist": {"salary": 200, "benefit": None},
    "baby_sitter": {"salary": 500, "benefit": "requires_3_children"},
}

# Gemstone Types
GEMSTONES = ["ruby", "sapphire", "emerald", "topaz", "onyx"]
GEMSTONE_FUSE_REWARD = 5000

# Crop Types & Seasons
CROPS = {
    "pepper": {"season": "spring", "growth_time": 7200, "buy_price": 50, "sell_price": 150, "order_price": 100},
    "potato": {"season": "autumn", "growth_time": 10800, "buy_price": 40, "sell_price": 120, "order_price": 80},
    "eggplant": {"season": "cloudy", "growth_time": 14400, "buy_price": 60, "sell_price": 180, "order_price": 120},
    "carrot": {"season": "winter", "growth_time": 5400, "buy_price": 30, "sell_price": 90, "order_price": 60},
    "corn": {"season": "all", "growth_time": 9000, "buy_price": 45, "sell_price": 135, "order_price": 90},
    "tomato": {"season": "all", "growth_time": 3600, "buy_price": 25, "sell_price": 75, "order_price": 50},
}

# Cooking Recipes
RECIPES = {
    "popcorn": {"ingredients": {"corn": 3}, "time": 600, "output": 1},
    "corn_flour": {"ingredients": {"corn": 5}, "time": 900, "output": 1},
    "fries": {"ingredients": {"potato": 3}, "time": 720, "output": 1},
    "chips": {"ingredients": {"potato": 5}, "time": 1080, "output": 1},
    "juice": {"ingredients": {"tomato": 10}, "time": 1200, "output": 1},
    "bread": {"ingredients": {"corn_flour": 5, "eggplant": 5}, "time": 1500, "output": 1},
    "salad": {"ingredients": {"carrot": 2, "tomato": 1}, "time": 900, "output": 1},
    "breadjam": {"ingredients": {"bread": 2, "tomato": 1}, "time": 1200, "output": 1},
    "sandwich": {"ingredients": {"bread": 1, "carrot": 5, "tomato": 1}, "time": 1800, "output": 1},
}

# Insurance Types
INSURANCE_TYPES = {
    "close_family": {"multiplier": 3},
    "family": {"multiplier": 2},
    "friend": {"multiplier": 1},
}

# Supported Languages
LANGUAGES = {
    "en": "English",
    "ru": "Russian",
    "fr": "French",
    "ua": "Ukrainian",
    "es": "Spanish",
    "de": "German",
    "zh": "Chinese",
    "it": "Italian",
}

# Animation Durations (seconds)
ANIMATIONS = {
    "marriage": 3,
    "adoption": 2,
    "divorce": 2,
    "rob_success": 2,
    "rob_fail": 2,
    "kill_success": 3,
    "daily_claim": 2,
    "gemstone_fuse": 3,
    "level_up": 3,
    "work_complete": 2,
    "harvest": 2,
    "cooking_done": 2,
    "game_win": 3,
    "game_lose": 2,
    "money_rain": 5,
    "new_friend": 2,
    "tree_growth": 2,
}

# UI Colors
COLORS = {
    "primary": "#4CAF50",
    "secondary": "#2196F3",
    "accent": "#FF9800",
    "danger": "#F44336",
    "success": "#8BC34A",
    "pink": "#E91E63",
    "blue": "#2196F3",
}

# Achievement Rarity Levels
ACHIEVEMENT_RARITY = ["bronze", "silver", "gold", "diamond", "platinum"]

# Referral Rewards
REFERRAL_REWARDS = {
    "referrer": 5000,
    "referred": 10000,
}

# VIP Tiers
VIP_TIERS = {
    "bronze": {"price": 5, "multiplier": 1.5},
    "silver": {"price": 10, "multiplier": 2},
    "gold": {"price": 25, "multiplier": 2.5},
    "diamond": {"price": 50, "multiplier": 3},
    "royal": {"price": 100, "multiplier": 4},
}

# Streak Rewards
STREAK_REWARDS = {
    1: {"money": 100},
    7: {"money": 1000, "bonus": True},
    30: {"money": 10000, "rare_item": True},
    100: {"money": 100000, "legendary_item": True},
    365: {"money": 1000000, "exclusive_badge": True},
}

# Mini Game Settings
GAMES = {
    "four_pics": {"timeout": 300, "reward_base": 50},
    "ripple": {"max_multiplier": 20},
    "nation": {"reward": 100},
    "trivia": {"cost": 5, "reward": 50, "timeout": 60},
    "lottery": {},
    "which_ai": {"reward": 25},
    "family_trivia": {"reward": 30},
    "paper_tactics": {},
    "crabs": {},
    "roulette": {},
    "sonar": {},
}

# Command Categories
COMMAND_CATEGORIES = {
    "family": ["/tree", "/adopt", "/marry", "/divorce", "/disown", "/runaway", "/relations", "/family", "/setpic", "/setpfp", "/customize", "/fulltree", "/bloodtree", "/makeparent", "/sibling"],
    "friend": ["/circle", "/friends", "/friend", "/unfriend", "/suggestions", "/flink", "/ratings", "/activefriends", "/fsearch"],
    "account": ["/account", "/profile", "/acc", "/me", "/bank", "/withdraw", "/deposit", "/weapon", "/rob", "/kill", "/donateblood", "/medical", "/insurance", "/pay", "/reputation", "/skills"],
    "daily": ["/daily", "/fuse", "/reactions", "/rxns", "/addgif", "/showgifs", "/remgifs"],
    "factory": ["/hire", "/factory", "/fire", "/buy shield", "/buy sword"],
    "garden": ["/garden", "/add", "/plant", "/harvest", "/sells", "/sell", "/barn", "/bn", "/buy boost", "/boost", "/refill", "/track", "/orders", "/gardens", "/fertilise"],
    "trading": ["/stands", "/putstand", "/stand", "/gift", "/alert"],
    "cooking": ["/cook", "/stove"],
    "games": ["/4p", "/fourpics", "/4h", "/4w", "/4s", "/ripple", "/rbet", "/rtake", "/bets", "/nation", "/question", "/lottery", "/whichai", "/ftrivia", "/paper", "/crabs", "/roulette", "/sonar"],
    "stats": ["/mb", "/moneyboard", "/leaderboard", "/moneygraph", "/mg", "/showstats", "/loadstats", "/interactions"],
    "utility": ["/2jpg", "/2png", "/lottie2gif", "/addcaption", "/2imgur", "/imagedl", "/bingreverse", "/figlet", "/qotd", "/shibapic", "/foodpic", "/joketype", "/randomjoke", "/dadjoke", "/evilinsult", "/randomadvice", "/ip2loc", "/shorten", "/name2gender", "/name2nation"],
    "extra": ["/waifu", "/waifus", "/waifugraph", "/setloc", "/setlocation", "/showmap", "/wedcard", "/refer", "/block", "/unblock", "/blocklist"],
    "settings": ["/disable", "/enable", "/disabled", "/toggle", "/gifs", "/incests", "/treemode", "/scope", "/autoprune", "/prune", "/setlang"],
}

# Admin Configuration
ADMIN_USER_IDS = list(map(int, os.getenv("ADMIN_USER_IDS", "123456789").split(",")))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = "bot.log"
