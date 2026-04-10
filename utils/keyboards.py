"""
Keyboard Builders for Fam Tree Bot
===================================
Inline and Reply keyboard builders
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from typing import List, Dict, Optional

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Get main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🌳 Family Tree", callback_data="menu_family"),
         InlineKeyboardButton("👥 Friends", callback_data="menu_friends")],
        [InlineKeyboardButton("💰 Account", callback_data="menu_account"),
         InlineKeyboardButton("🌱 Garden", callback_data="menu_garden")],
        [InlineKeyboardButton("🏭 Factory", callback_data="menu_factory"),
         InlineKeyboardButton("🎮 Games", callback_data="menu_games")],
        [InlineKeyboardButton("🏪 Marketplace", callback_data="menu_market"),
         InlineKeyboardButton("📊 Stats", callback_data="menu_stats")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="menu_settings"),
         InlineKeyboardButton("❓ Help", callback_data="menu_help")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_family_menu_keyboard() -> InlineKeyboardMarkup:
    """Get family menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🌳 View Tree", callback_data="family_tree"),
         InlineKeyboardButton("👨‍👩‍👧 Relations", callback_data="family_relations")],
        [InlineKeyboardButton("💍 Marry", callback_data="family_marry"),
         InlineKeyboardButton("👶 Adopt", callback_data="family_adopt")],
        [InlineKeyboardButton("💔 Divorce", callback_data="family_divorce"),
         InlineKeyboardButton("🚪 Disown", callback_data="family_disown")],
        [InlineKeyboardButton("🖼️ Set Picture", callback_data="family_setpic"),
         InlineKeyboardButton("✨ Customize", callback_data="family_customize")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_confirmation_keyboard(yes_callback: str, no_callback: str) -> InlineKeyboardMarkup:
    """Get yes/no confirmation keyboard"""
    keyboard = [
        [InlineKeyboardButton("✅ Yes", callback_data=yes_callback),
         InlineKeyboardButton("❌ No", callback_data=no_callback)],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_account_keyboard() -> InlineKeyboardMarkup:
    """Get account menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🏦 Bank", callback_data="account_bank"),
         InlineKeyboardButton("🔫 Weapons", callback_data="account_weapons")],
        [InlineKeyboardButton("🛡️ Insurance", callback_data="account_insurance"),
         InlineKeyboardButton("💼 Jobs", callback_data="account_jobs")],
        [InlineKeyboardButton("📊 Statistics", callback_data="account_stats"),
         InlineKeyboardButton("🏆 Achievements", callback_data="account_achievements")],
        [InlineKeyboardButton("💰 Daily Bonus", callback_data="account_daily"),
         InlineKeyboardButton("💎 Fuse Gems", callback_data="account_fuse")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_weapons_keyboard() -> InlineKeyboardMarkup:
    """Get weapons selection keyboard"""
    keyboard = [
        [InlineKeyboardButton("👊 Punch (Free)", callback_data="weapon_punch")],
        [InlineKeyboardButton("🔪 Blade ($100)", callback_data="weapon_blade")],
        [InlineKeyboardButton("⚔️ Sword ($200)", callback_data="weapon_sword")],
        [InlineKeyboardButton("🔫 Pistol ($400)", callback_data="weapon_pistol")],
        [InlineKeyboardButton("🔫 Gun ($500)", callback_data="weapon_gun")],
        [InlineKeyboardButton("🏹 Bow ($5,000)", callback_data="weapon_bow")],
        [InlineKeyboardButton("☠️ Poison ($8,000)", callback_data="weapon_poison")],
        [InlineKeyboardButton("🚀 Rocket Launcher ($10,000)", callback_data="weapon_rocket_launcher")],
        [InlineKeyboardButton("🔙 Back", callback_data="account_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_garden_keyboard(plots: List[Dict]) -> InlineKeyboardMarkup:
    """Get garden action keyboard"""
    keyboard = [
        [InlineKeyboardButton("🌱 Plant", callback_data="garden_plant"),
         InlineKeyboardButton("🌾 Harvest", callback_data="garden_harvest")],
        [InlineKeyboardButton("⚡ Boost", callback_data="garden_boost"),
         InlineKeyboardButton("🏚️ Barn", callback_data="garden_barn")],
        [InlineKeyboardButton("📋 Orders", callback_data="garden_orders"),
         InlineKeyboardButton("🏪 Stands", callback_data="garden_stands")],
        [InlineKeyboardButton("📊 Track", callback_data="garden_track"),
         InlineKeyboardButton("🔄 Refill", callback_data="garden_refill")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_crop_selection_keyboard() -> InlineKeyboardMarkup:
    """Get crop selection keyboard"""
    keyboard = [
        [InlineKeyboardButton("🌶️ Pepper ($50)", callback_data="crop_pepper")],
        [InlineKeyboardButton("🥔 Potato ($40)", callback_data="crop_potato")],
        [InlineKeyboardButton("🍆 Eggplant ($60)", callback_data="crop_eggplant")],
        [InlineKeyboardButton("🥕 Carrot ($30)", callback_data="crop_carrot")],
        [InlineKeyboardButton("🌽 Corn ($45)", callback_data="crop_corn")],
        [InlineKeyboardButton("🍅 Tomato ($25)", callback_data="crop_tomato")],
        [InlineKeyboardButton("🔙 Back", callback_data="garden_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_factory_keyboard(workers: List[Dict]) -> InlineKeyboardMarkup:
    """Get factory management keyboard"""
    keyboard = []
    
    for i, worker in enumerate(workers[:5]):
        status = worker.get('status', 'idle')
        worker_id = worker.get('id')
        
        if status == 'idle':
            keyboard.append([InlineKeyboardButton(
                f"👷 Worker {i+1}: Send to Work", 
                callback_data=f"factory_work_{worker_id}")])
        elif status == 'working':
            keyboard.append([InlineKeyboardButton(
                f"👷 Worker {i+1}: Working...", 
                callback_data=f"factory_status_{worker_id}")])
        elif status == 'completed':
            keyboard.append([InlineKeyboardButton(
                f"👷 Worker {i+1}: Collect Reward ✓", 
                callback_data=f"factory_collect_{worker_id}")])
    
    keyboard.extend([
        [InlineKeyboardButton("🛡️ Buy Shield", callback_data="factory_buy_shield"),
         InlineKeyboardButton("⚔️ Buy Sword", callback_data="factory_buy_sword")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
    ])
    return InlineKeyboardMarkup(keyboard)

def get_games_keyboard() -> InlineKeyboardMarkup:
    """Get games menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🖼️ 4 Pics 1 Word", callback_data="game_4pics"),
         InlineKeyboardButton("🌊 Ripple", callback_data="game_ripple")],
        [InlineKeyboardButton("🌍 Nation Guess", callback_data="game_nation"),
         InlineKeyboardButton("❓ Trivia", callback_data="game_trivia")],
        [InlineKeyboardButton("🎰 Lottery", callback_data="game_lottery"),
         InlineKeyboardButton("🤖 Which AI?", callback_data="game_whichai")],
        [InlineKeyboardButton("🎲 Roulette", callback_data="game_roulette"),
         InlineKeyboardButton("🦀 Crabs", callback_data="game_crabs")],
        [InlineKeyboardButton("📝 Family Trivia", callback_data="game_ftrivia"),
         InlineKeyboardButton("📄 Paper Tactics", callback_data="game_paper")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_market_keyboard() -> InlineKeyboardMarkup:
    """Get marketplace keyboard"""
    keyboard = [
        [InlineKeyboardButton("🌽 Corn", callback_data="market_corn"),
         InlineKeyboardButton("🥔 Potato", callback_data="market_potato")],
        [InlineKeyboardButton("🍆 Eggplant", callback_data="market_eggplant"),
         InlineKeyboardButton("🥕 Carrot", callback_data="market_carrot")],
        [InlineKeyboardButton("🍅 Tomato", callback_data="market_tomato"),
         InlineKeyboardButton("🌶️ Pepper", callback_data="market_pepper")],
        [InlineKeyboardButton("🏪 My Stand", callback_data="market_mystand"),
         InlineKeyboardButton("➕ Sell Items", callback_data="market_sell")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_stats_keyboard() -> InlineKeyboardMarkup:
    """Get statistics keyboard"""
    keyboard = [
        [InlineKeyboardButton("💰 Money Board", callback_data="stats_money"),
         InlineKeyboardButton("📈 Money Graph", callback_data="stats_graph")],
        [InlineKeyboardButton("👨‍👩‍👧 Family Leaderboard", callback_data="stats_family"),
         InlineKeyboardButton("📊 My Stats", callback_data="stats_mystats")],
        [InlineKeyboardButton("🤝 Interactions", callback_data="stats_interactions"),
         InlineKeyboardButton("🏆 Achievements", callback_data="stats_achievements")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_settings_keyboard() -> InlineKeyboardMarkup:
    """Get settings keyboard"""
    keyboard = [
        [InlineKeyboardButton("🌐 Language", callback_data="settings_language"),
         InlineKeyboardButton("🌳 Tree Scope", callback_data="settings_scope")],
        [InlineKeyboardButton("🔔 Notifications", callback_data="settings_notifications"),
         InlineKeyboardButton("🎨 Theme", callback_data="settings_theme")],
        [InlineKeyboardButton("⚙️ Toggle Features", callback_data="settings_toggle"),
         InlineKeyboardButton("🗑️ Auto Prune", callback_data="settings_prune")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_language_keyboard() -> InlineKeyboardMarkup:
    """Get language selection keyboard"""
    keyboard = [
        [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("🇫🇷 Français", callback_data="lang_fr")],
        [InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es")],
        [InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de")],
        [InlineKeyboardButton("🇮🇹 Italiano", callback_data="lang_it")],
        [InlineKeyboardButton("🇨🇳 中文", callback_data="lang_zh")],
        [InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_ua")],
        [InlineKeyboardButton("🔙 Back", callback_data="settings_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_jobs_keyboard() -> InlineKeyboardMarkup:
    """Get jobs selection keyboard"""
    keyboard = [
        [InlineKeyboardButton("❌ Unemployed ($0)", callback_data="job_unemployed")],
        [InlineKeyboardButton("🏦 Banker ($100)", callback_data="job_banker")],
        [InlineKeyboardButton("👮 Policeman ($100)", callback_data="job_policeman")],
        [InlineKeyboardButton("👨‍⚕️ Doctor ($300)", callback_data="job_doctor")],
        [InlineKeyboardButton("🔬 Scientist ($200)", callback_data="job_scientist")],
        [InlineKeyboardButton("👶 Baby Sitter ($500)", callback_data="job_baby_sitter")],
        [InlineKeyboardButton("🔙 Back", callback_data="account_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_bank_keyboard() -> InlineKeyboardMarkup:
    """Get bank menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("💰 Deposit", callback_data="bank_deposit"),
         InlineKeyboardButton("💸 Withdraw", callback_data="bank_withdraw")],
        [InlineKeyboardButton("📊 Balance", callback_data="bank_balance"),
         InlineKeyboardButton("📜 History", callback_data="bank_history")],
        [InlineKeyboardButton("🔙 Back", callback_data="account_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_reactions_keyboard() -> InlineKeyboardMarkup:
    """Get reactions keyboard"""
    keyboard = [
        [InlineKeyboardButton("🤗 Hug", callback_data="rxn_hug"),
         InlineKeyboardButton("🤚 Pat", callback_data="rxn_pat")],
        [InlineKeyboardButton("😘 Kiss", callback_data="rxn_kiss"),
         InlineKeyboardButton("😢 Sad", callback_data="rxn_sad")],
        [InlineKeyboardButton("😊 Smile", callback_data="rxn_smile"),
         InlineKeyboardButton("😭 Cry", callback_data="rxn_cry")],
        [InlineKeyboardButton("👋 Slap", callback_data="rxn_slap"),
         InlineKeyboardButton("👉 Poke", callback_data="rxn_poke")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_combat_keyboard(target_id: int) -> InlineKeyboardMarkup:
    """Get combat action keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔫 Rob", callback_data=f"combat_rob_{target_id}"),
         InlineKeyboardButton("💀 Kill", callback_data=f"combat_kill_{target_id}")],
        [InlineKeyboardButton("❤️ Donate Blood", callback_data=f"combat_donate_{target_id}")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_ripple_game_keyboard(multiplier: float, bet: float) -> InlineKeyboardMarkup:
    """Get Ripple betting game keyboard"""
    potential_win = bet * multiplier
    keyboard = [
        [InlineKeyboardButton(f"🌻 Step (1.5×) - Win: ${potential_win * 1.5:.0f}", callback_data="ripple_step")],
        [InlineKeyboardButton(f"💰 Take - Win: ${potential_win:.0f}", callback_data="ripple_take")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_pagination_keyboard(current_page: int, total_pages: int, base_callback: str) -> InlineKeyboardMarkup:
    """Get pagination keyboard"""
    keyboard = []
    row = []
    
    if current_page > 1:
        row.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"{base_callback}_{current_page - 1}"))
    
    row.append(InlineKeyboardButton(f"{current_page}/{total_pages}", callback_data="noop"))
    
    if current_page < total_pages:
        row.append(InlineKeyboardButton("Next ➡️", callback_data=f"{base_callback}_{current_page + 1}"))
    
    keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def get_admin_keyboard() -> InlineKeyboardMarkup:
    """Get admin panel keyboard"""
    keyboard = [
        [InlineKeyboardButton("📊 Statistics", callback_data="admin_stats"),
         InlineKeyboardButton("👥 Users", callback_data="admin_users")],
        [InlineKeyboardButton("💰 Economy", callback_data="admin_economy"),
         InlineKeyboardButton("🎁 Give", callback_data="admin_give")],
        [InlineKeyboardButton("🔨 Ban", callback_data="admin_ban"),
         InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton("🔧 Maintenance", callback_data="admin_maintenance"),
         InlineKeyboardButton("📋 Logs", callback_data="admin_logs")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def build_inline_keyboard(buttons: List[List[Dict]]) -> InlineKeyboardMarkup:
    """Build custom inline keyboard from button data"""
    keyboard = []
    for row in buttons:
        keyboard_row = []
        for btn in row:
            keyboard_row.append(InlineKeyboardButton(
                text=btn.get('text', 'Button'),
                callback_data=btn.get('callback_data', 'noop'),
                url=btn.get('url')
            ))
        keyboard.append(keyboard_row)
    return InlineKeyboardMarkup(keyboard)
