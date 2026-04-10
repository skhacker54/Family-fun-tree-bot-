"""
Utility Helpers for Fam Tree Bot
=================================
Helper functions and utilities
"""

import random
import string
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from telegram import User as TelegramUser

# Language translations
TRANSLATIONS = {
    "en": {
        "welcome": "Welcome to Fam Tree Bot! 🌳\nYour ultimate family simulation RPG experience.",
        "balance": "Balance: ${:,}",
        "no_user": "User not found!",
        "insufficient_funds": "Insufficient funds!",
        "success": "Success! ✅",
        "error": "An error occurred! ❌",
        "cooldown": "Please wait {} before trying again.",
        "dead": "You are dead! Use /medical to revive ($500)",
    },
    "ru": {
        "welcome": "Добро пожаловать в Fam Tree Bot! 🌳\nВаше лучшее семейное RPG.",
        "balance": "Баланс: ${:,}",
        "no_user": "Пользователь не найден!",
        "insufficient_funds": "Недостаточно средств!",
        "success": "Успех! ✅",
        "error": "Произошла ошибка! ❌",
        "cooldown": "Пожалуйста, подождите {} перед повторной попыткой.",
        "dead": "Вы мертвы! Используйте /medical для возрождения ($500)",
    },
    "fr": {
        "welcome": "Bienvenue sur Fam Tree Bot! 🌳\nVotre expérience RPG familiale ultime.",
        "balance": "Solde: ${:,}",
        "no_user": "Utilisateur non trouvé!",
        "insufficient_funds": "Fonds insuffisants!",
        "success": "Succès! ✅",
        "error": "Une erreur s'est produite! ❌",
        "cooldown": "Veuillez attendre {} avant de réessayer.",
        "dead": "Vous êtes mort! Utilisez /medical pour ressusciter ($500)",
    },
    "es": {
        "welcome": "¡Bienvenido a Fam Tree Bot! 🌳\nTu experiencia RPG familiar definitiva.",
        "balance": "Saldo: ${:,}",
        "no_user": "¡Usuario no encontrado!",
        "insufficient_funds": "¡Fondos insuficientes!",
        "success": "¡Éxito! ✅",
        "error": "¡Ocurrió un error! ❌",
        "cooldown": "Por favor espere {} antes de intentar de nuevo.",
        "dead": "¡Estás muerto! Usa /medical para revivir ($500)",
    },
    "de": {
        "welcome": "Willkommen bei Fam Tree Bot! 🌳\nDein ultimatives Familien-RPG-Erlebnis.",
        "balance": "Guthaben: ${:,}",
        "no_user": "Benutzer nicht gefunden!",
        "insufficient_funds": "Unzureichende Mittel!",
        "success": "Erfolg! ✅",
        "error": "Ein Fehler ist aufgetreten! ❌",
        "cooldown": "Bitte warten Sie {} vor dem nächsten Versuch.",
        "dead": "Du bist tot! Benutze /medical zum Wiederbeleben ($500)",
    },
    "it": {
        "welcome": "Benvenuto in Fam Tree Bot! 🌳\nLa tua esperienza RPG familiare definitiva.",
        "balance": "Saldo: ${:,}",
        "no_user": "Utente non trovato!",
        "insufficient_funds": "Fondi insufficienti!",
        "success": "Successo! ✅",
        "error": "Si è verificato un errore! ❌",
        "cooldown": "Attendi {} prima di riprovare.",
        "dead": "Sei morto! Usa /medical per resuscitare ($500)",
    },
    "zh": {
        "welcome": "欢迎使用 Fam Tree Bot! 🌳\n您终极的家庭模拟RPG体验。",
        "balance": "余额: ${:,}",
        "no_user": "用户未找到!",
        "insufficient_funds": "资金不足!",
        "success": "成功! ✅",
        "error": "发生错误! ❌",
        "cooldown": "请等待{}后再试。",
        "dead": "你已死亡! 使用 /medical 复活 ($500)",
    },
    "ua": {
        "welcome": "Ласкаво просимо до Fam Tree Bot! 🌳\nВаше найкраще сімейне RPG.",
        "balance": "Баланс: ${:,}",
        "no_user": "Користувача не знайдено!",
        "insufficient_funds": "Недостатньо коштів!",
        "success": "Успіх! ✅",
        "error": "Сталася помилка! ❌",
        "cooldown": "Будь ласка, зачекайте {} перед повторною спробою.",
        "dead": "Ви мертві! Використовуйте /medical для відродження ($500)",
    },
}

def get_text(key: str, lang: str = 'en', **kwargs) -> str:
    """Get translated text"""
    translation = TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, TRANSLATIONS['en'].get(key, key))
    return translation.format(**kwargs)

def generate_referral_code(telegram_id: int) -> str:
    """Generate unique referral code"""
    return f"ref_{telegram_id}_{random.randint(1000, 9999)}"

def format_money(amount: float) -> str:
    """Format money with commas"""
    return f"${amount:,.0f}"

def format_time(seconds: int) -> str:
    """Format seconds to readable time"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

def get_current_season() -> str:
    """Get current season based on month"""
    month = datetime.now().month
    if month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    elif month in [9, 10, 11]:
        return "autumn"
    else:
        return "winter"

def calculate_daily_reward(family_count: int, job_salary: int) -> int:
    """Calculate daily reward based on family and job"""
    base = 100
    family_bonus = family_count * 50
    return base + family_bonus + job_salary

def get_random_gemstone() -> str:
    """Get random gemstone type"""
    gemstones = ["ruby", "sapphire", "emerald", "topaz", "onyx"]
    return random.choice(gemstones)

def calculate_worker_price(rating: int, money: float) -> float:
    """Calculate worker price based on stats"""
    base_price = 1000
    rating_factor = rating * 10
    money_factor = min(money * 0.1, 1000)
    return base_price + rating_factor + money_factor

def can_rob(robber_health: int, robber_dead: bool, target_dead: bool) -> tuple:
    """Check if robbery is possible"""
    if robber_dead:
        return False, "You cannot rob while dead!"
    if robber_health <= 0:
        return False, "You need at least 1 health to rob!"
    if target_dead:
        return False, "Cannot rob a dead person!"
    return True, ""

def can_kill(killer_health: int, killer_dead: bool, target_dead: bool) -> tuple:
    """Check if kill is possible"""
    if killer_dead:
        return False, "You cannot kill while dead!"
    if killer_health <= 0:
        return False, "You need at least 1 health to kill!"
    if target_dead:
        return False, "Target is already dead!"
    return True, ""

def calculate_rob_amount(target_balance: float, is_rich: bool = False) -> float:
    """Calculate robbery amount"""
    base = random.randint(50, 200)
    if is_rich or target_balance > 10000:
        base = random.randint(100, 1000)
    return min(base, target_balance * 0.1)

def calculate_insurance_payout(insurance_type: str, base_amount: float) -> float:
    """Calculate insurance payout"""
    multipliers = {
        "close_family": 3,
        "family": 2,
        "friend": 1,
    }
    return base_amount * multipliers.get(insurance_type, 1)

def create_progress_bar(current: int, total: int, length: int = 20) -> str:
    """Create ASCII progress bar"""
    filled = int(length * current / total)
    bar = '█' * filled + '░' * (length - filled)
    return f"[{bar}] {current}/{total}"

def generate_tree_visual(family_data: List[Dict]) -> str:
    """Generate ASCII family tree visualization"""
    if not family_data:
        return "🌳 Your family tree is empty!"
    
    tree = "```\n🌳 FAMILY TREE\n"
    tree += "══════════════\n\n"
    
    for member in family_data:
        relation = member.get('relation', 'Unknown')
        username = member.get('username', 'Unknown')
        tree += f"  ├─ {relation}: @{username}\n"
    
    tree += "```"
    return tree

def format_profile_card(user_data: Dict) -> str:
    """Format user profile card"""
    card = f"""
┌─────────────────────────────────────────┐
│ 👤 USER PROFILE                         │
├─────────────────────────────────────────┤
│                                         │
│  @{user_data.get('username', 'Unknown')}           │
│                                         │
│  💰 {format_money(user_data.get('balance', 0))}                │
│  ⭐ Reputation: {user_data.get('reputation', 0)}/200     │
│  💼 Job: {user_data.get('job', 'Unemployed').title()}              │
│                                         │
│  💎 Gemstone: {user_data.get('gemstone', 'None').title()}           │
│  🔫 Weapon: {user_data.get('weapon', 'Punch').title()}          │
│  🛡️ Insurance: {user_data.get('insurance_count', 0)} Active        │
│  ❤️ Health: {user_data.get('health', 5)}/5 Hearts            │
│                                         │
│  [🏦 Bank] [🔫 Weapons] [💼 Jobs]       │
│  [🛡️ Insurance] [📊 Stats]              │
└─────────────────────────────────────────┘
"""
    return card

def format_garden_visual(plots: List[Dict]) -> str:
    """Format garden visualization"""
    garden = "```\n🌱 YOUR GARDEN\n"
    garden += f"Season: {get_current_season().title()}\n"
    garden += "════════════════\n\n"
    
    for i, plot in enumerate(plots, 1):
        if plot.get('is_empty'):
            status = "[Emp]"
        elif plot.get('is_ready'):
            status = "[Rdy]"
        else:
            remaining = plot.get('remaining_time', 0)
            status = f"[{format_time(remaining)}]"
        
        crop = plot.get('crop_type', 'Empty')
        garden += f"  {i}. {status} {crop.title()}\n"
    
    garden += "\n[🌱 Plant] [🌾 Harvest] [⚡ Boost]\n"
    garden += "[🏚️ Barn] [📋 Orders] [🏪 Stands]\n"
    garden += "```"
    return garden

def format_factory_dashboard(workers: List[Dict], rating: int) -> str:
    """Format factory dashboard"""
    dashboard = f"""
┌─────────────────────────────────────────┐
│ 🏭 YOUR FACTORY                         │
├─────────────────────────────────────────┤
│                                         │
│  ⭐ Rating: {rating}                    │
│                                         │
│  WORKERS:                               │
"""
    for i, worker in enumerate(workers, 1):
        username = worker.get('username', 'Unknown')
        status = worker.get('status', 'Idle')
        if status == 'working':
            remaining = worker.get('remaining_time', 0)
            status_str = f"Working ({format_time(remaining)} left)"
        elif status == 'completed':
            status_str = "Completed ✓"
        else:
            status_str = "Idle [Send to Work]"
        dashboard += f"│  {i}. @{username} - {status_str}\n"
    
    dashboard += "│                                         │\n"
    dashboard += "│  [🛡️ Shields] [⚔️ Swords]              │\n"
    dashboard += "└─────────────────────────────────────────┘"
    return dashboard

def format_money_leaderboard(users: List[Dict]) -> str:
    """Format money leaderboard"""
    if not users:
        return "No data available!"
    
    board = "```\n💰 RICHEST IN CHAT\n"
    board += "══════════════════\n\n"
    
    medals = ["🥇", "🥈", "🥉"]
    for i, user in enumerate(users[:10], 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        username = user.get('username', 'Unknown')
        balance = format_money(user.get('balance', 0))
        board += f"{medal} {username} - {balance}\n"
    
    board += "```"
    return board

def parse_amount_expression(expression: str, user_balance: float) -> float:
    """Parse amount expression (supports +, -, *, /, 'all', 'half')"""
    expression = expression.lower().strip()
    
    if expression == 'all':
        return user_balance
    if expression == 'half':
        return user_balance / 2
    
    try:
        # Replace 'k' with 1000
        expression = expression.replace('k', '*1000')
        # Safe eval for math expressions
        result = eval(expression, {"__builtins__": {}}, {})
        return float(result)
    except:
        try:
            return float(expression)
        except:
            return 0

def get_user_mention(user_id: int, username: str = None, first_name: str = None) -> str:
    """Get user mention for Telegram"""
    if username:
        return f"@{username}"
    return f"[{first_name or 'User'}](tg://user?id={user_id})"

def escape_markdown(text: str) -> str:
    """Escape markdown characters"""
    chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in chars:
        text = text.replace(char, f'\\{char}')
    return text

def generate_random_id(length: int = 10) -> str:
    """Generate random ID"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def is_new_day(last_reset: datetime) -> bool:
    """Check if it's a new day since last reset"""
    if not last_reset:
        return True
    now = datetime.utcnow()
    return now.date() != last_reset.date()

def calculate_time_remaining(end_time: datetime) -> int:
    """Calculate remaining seconds until end_time"""
    if not end_time:
        return 0
    remaining = (end_time - datetime.utcnow()).total_seconds()
    return max(0, int(remaining))

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """Split list into chunks"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def get_random_joke() -> str:
    """Get random joke"""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "What do you call a fake noodle? An impasta!",
        "Why did the math book look sad? Because it had too many problems!",
    ]
    return random.choice(jokes)

def get_dad_joke() -> str:
    """Get dad joke"""
    jokes = [
        "I'm afraid for the calendar. Its days are numbered.",
        "Singing in the shower is fun until you get soap in your mouth. Then it's a soap opera.",
        "What do a tick and the Eiffel Tower have in common? They're both Paris sites.",
        "How do you follow Will Smith in the snow? You follow the fresh prints.",
        "I thought the dryer was shrinking my clothes. Turns out it was the refrigerator all along.",
    ]
    return random.choice(jokes)

def get_evil_insult() -> str:
    """Get playful insult"""
    insults = [
        "You're not stupid; you just have bad luck thinking.",
        "I'd agree with you but then we'd both be wrong.",
        "You're not dumb. You just have bad luck when it comes to thinking.",
        "I'm not saying you're stupid, I'm just saying you have bad luck when it comes to thinking.",
        "You're like a cloud. When you disappear, it's a beautiful day.",
    ]
    return random.choice(insults)

def get_random_advice() -> str:
    """Get random life advice"""
    advice = [
        "Believe in yourself! You are capable of amazing things.",
        "Take time to appreciate the small things in life.",
        "Don't be afraid to ask for help when you need it.",
        "Every day is a new opportunity to be better.",
        "Kindness costs nothing but means everything.",
    ]
    return random.choice(advice)

def get_quote_of_the_day() -> str:
    """Get quote of the day"""
    quotes = [
        '"The only way to do great work is to love what you do." - Steve Jobs',
        '"Believe you can and you\'re halfway there." - Theodore Roosevelt',
        '"The future belongs to those who believe in the beauty of their dreams." - Eleanor Roosevelt',
        '"Success is not final, failure is not fatal: it is the courage to continue that counts." - Winston Churchill',
        '"The only limit to our realization of tomorrow will be our doubts of today." - Franklin D. Roosevelt',
    ]
    return random.choice(quotes)
