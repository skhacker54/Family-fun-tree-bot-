"""
Game Commands and Mini-Games Handlers
======================================
All game-related commands
"""

import random
import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from models.database import *
from config.settings import *
from utils.helpers import *
from utils.keyboards import *
from handlers.commands import get_db, get_or_create_user

# Game data storage (in-memory for active games)
active_games = {}

# ==================== MODULE 9: MINI GAMES ====================

async def fourpics_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /4p command (4 Pics 1 Word)"""
    user_id = update.effective_user.id
    
    # Word list for the game
    words = [
        ("BALL", "🏀⚽🎾🏐"),
        ("FIRE", "🔥🚒🧯🕯️"),
        ("WATER", "💧🌊🚰🏊"),
        ("TREE", "🌳🌲🎄🌴"),
        ("HEART", "❤️💕💖💗"),
        ("STAR", "⭐🌟✨💫"),
        ("MUSIC", "🎵🎶🎸🎹"),
        ("FOOD", "🍕🍔🍟🌮"),
        ("BOOK", "📚📖📕📗"),
        ("PHONE", "📱☎️📞📲"),
    ]
    
    word, emojis = random.choice(words)
    scrambled = ''.join(random.sample(word, len(word)))
    
    # Store game data
    active_games[user_id] = {
        'game': '4pics',
        'word': word,
        'start_time': datetime.utcnow()
    }
    
    await update.message.reply_text(
        f"🖼️ *4 PICS 1 WORD*\n"
        f"═══════════════════\n\n"
        f"{emojis}\n\n"
        f"Letters: *{scrambled}*\n\n"
        f"Type your guess!\n"
        f"⏱️ You have 5 minutes!",
        parse_mode=ParseMode.MARKDOWN
    )

async def ripple_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ripple command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not context.args:
            await update.message.reply_text(
                "❌ Usage: /ripple [bet_amount]\n"
                "Example: /ripple 100"
            )
            return
        
        try:
            bet = float(context.args[0])
        except:
            await update.message.reply_text("❌ Invalid bet amount!")
            return
        
        if bet <= 0:
            await update.message.reply_text("❌ Bet must be positive!")
            return
        
        if bet > user.balance:
            await update.message.reply_text("❌ Insufficient funds!")
            return
        
        user_id = update.effective_user.id
        active_games[user_id] = {
            'game': 'ripple',
            'bet': bet,
            'multiplier': 1.0,
            'status': 'active'
        }
        
        await update.message.reply_text(
            f"🌊 *RIPPLE BETTING*\n"
            f"═══════════════════\n\n"
            f"💰 Bet: ${bet:,.0f}\n"
            f"📈 Multiplier: 1.0×\n"
            f"💵 Potential Win: ${bet:,.0f}\n\n"
            f"Choose your path:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_ripple_game_keyboard(1.0, bet)
        )
    finally:
        session.close()

async def nation_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /nation command"""
    countries = {
        "france": "🇫🇷",
        "germany": "🇩🇪",
        "italy": "🇮🇹",
        "spain": "🇪🇸",
        "japan": "🇯🇵",
        "brazil": "🇧🇷",
        "canada": "🇨🇦",
        "australia": "🇦🇺",
        "mexico": "🇲🇽",
        "india": "🇮🇳",
    }
    
    country, flag = random.choice(list(countries.items()))
    
    user_id = update.effective_user.id
    active_games[user_id] = {
        'game': 'nation',
        'answer': country,
        'start_time': datetime.utcnow()
    }
    
    await update.message.reply_text(
        f"🌍 *GUESS THE NATION*\n"
        f"═══════════════════\n\n"
        f"Flag: {flag}\n\n"
        f"Which country is this?\n\n"
        f"💰 Reward: $100",
        parse_mode=ParseMode.MARKDOWN
    )

async def question_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /question command (Trivia)"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        cost = 5
        if user.balance < cost:
            await update.message.reply_text(f"❌ You need ${cost} to play!")
            return
        
        trivia_questions = [
            ("What is the capital of France?", "paris", ["london", "berlin", "madrid"]),
            ("What is 2 + 2?", "4", ["3", "5", "6"]),
            ("What planet is known as the Red Planet?", "mars", ["venus", "jupiter", "saturn"]),
            ("Who painted the Mona Lisa?", "leonardo da vinci", ["picasso", "van gogh", "michelangelo"]),
            ("What is the largest ocean?", "pacific", ["atlantic", "indian", "arctic"]),
        ]
        
        question, answer, wrong = random.choice(trivia_questions)
        
        user.balance -= cost
        session.commit()
        
        user_id = update.effective_user.id
        active_games[user_id] = {
            'game': 'trivia',
            'answer': answer,
            'start_time': datetime.utcnow()
        }
        
        options = [answer] + wrong
        random.shuffle(options)
        
        keyboard = []
        for opt in options:
            keyboard.append([InlineKeyboardButton(opt.title(), callback_data=f"trivia_{opt}")])
        
        await update.message.reply_text(
            f"❓ *TRIVIA*\n"
            f"═══════════════════\n\n"
            f"{question}\n\n"
            f"💰 Cost: ${cost}\n"
            f"💵 Reward: $50\n"
            f"⏱️ 60 seconds!",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    finally:
        session.close()

async def lottery_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /lottery command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not context.args:
            await update.message.reply_text(
                "❌ Usage: /lottery [amount]\n"
                "Example: /lottery 50"
            )
            return
        
        try:
            amount = float(context.args[0])
        except:
            await update.message.reply_text("❌ Invalid amount!")
            return
        
        if amount <= 0:
            await update.message.reply_text("❌ Amount must be positive!")
            return
        
        if amount > user.balance:
            await update.message.reply_text("❌ Insufficient funds!")
            return
        
        # Simple lottery - 10% chance to win 5x
        user.balance -= amount
        
        if random.random() < 0.1:
            winnings = amount * 5
            user.balance += winnings
            session.commit()
            await update.message.reply_text(
                f"🎰 *LOTTERY WIN!*\n\n"
                f"🎉 Congratulations!\n"
                f"💰 You won {format_money(winnings)}!"
            )
        else:
            session.commit()
            await update.message.reply_text(
                f"🎰 *LOTTERY*\n\n"
                f"😔 Better luck next time!\n"
                f"💰 You lost {format_money(amount)}"
            )
    finally:
        session.close()

async def whichai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /whichai command"""
    await update.message.reply_text(
        f"🤖 *WHICH AI?*\n"
        f"═══════════════════\n\n"
        f"🎨 Two images will be shown...\n"
        f"Guess which one is AI-generated!\n\n"
        f"💰 Reward: $25\n\n"
        f"[Left] or [Right]?",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Left", callback_data="whichai_left"),
             InlineKeyboardButton("Right ➡️", callback_data="whichai_right")]
        ])
    )

async def ftrivia_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ftrivia command (Family Trivia)"""
    questions = [
        ("What do you call your parent's brother?", "uncle"),
        ("What do you call your sibling's child?", "niece/nephew"),
        ("What is the term for your spouse's mother?", "mother-in-law"),
        ("What do you call your child's child?", "grandchild"),
        ("What is the term for your parent's parent?", "grandparent"),
    ]
    
    question, answer = random.choice(questions)
    
    user_id = update.effective_user.id
    active_games[user_id] = {
        'game': 'ftrivia',
        'answer': answer,
        'start_time': datetime.utcnow()
    }
    
    await update.message.reply_text(
        f"👨‍👩‍👧 *FAMILY TRIVIA*\n"
        f"═══════════════════\n\n"
        f"{question}\n\n"
        f"💰 Reward: $30",
        parse_mode=ParseMode.MARKDOWN
    )

async def paper_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /paper command (Paper Tactics)"""
    await update.message.reply_text(
        f"📄 *PAPER TACTICS*\n"
        f"═══════════════════\n\n"
        f"Grid-based tactical game coming soon!\n\n"
        f"Challenge a friend by replying to them!",
        parse_mode=ParseMode.MARKDOWN
    )

async def crabs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /crabs command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        # Simple crab growing game
        crabs = random.randint(1, 5)
        value = crabs * 50
        
        user.balance += value
        session.commit()
        
        await update.message.reply_text(
            f"🦀 *CRAB GROWING*\n\n"
            f"You grew {crabs} crabs!\n"
            f"💰 Earned: ${value}"
        )
    finally:
        session.close()

async def roulette_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /roulette command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not context.args:
            await update.message.reply_text(
                "❌ Usage: /roulette [bet] [red/black/green]\n"
                "Example: /roulette 100 red"
            )
            return
        
        try:
            bet = float(context.args[0])
            color = context.args[1].lower()
        except:
            await update.message.reply_text("❌ Invalid bet or color!")
            return
        
        if bet > user.balance:
            await update.message.reply_text("❌ Insufficient funds!")
            return
        
        user.balance -= bet
        
        # Roulette: 18 red, 18 black, 2 green (European)
        result = random.randint(0, 36)
        if result == 0:
            result_color = "green"
        elif result % 2 == 1:
            result_color = "red"
        else:
            result_color = "black"
        
        if color == result_color:
            if color == "green":
                winnings = bet * 14
            else:
                winnings = bet * 2
            user.balance += winnings
            session.commit()
            await update.message.reply_text(
                f"🎰 *ROULETTE: {result} {result_color.upper()}*\n\n"
                f"🎉 You won {format_money(winnings)}!"
            )
        else:
            session.commit()
            await update.message.reply_text(
                f"🎰 *ROULETTE: {result} {result_color.upper()}*\n\n"
                f"😔 You lost {format_money(bet)}!"
            )
    finally:
        session.close()

async def sonar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /sonar command"""
    await update.message.reply_text(
        f"📡 *SONAR MINIGAME*\n"
        f"═══════════════════\n\n"
        f"Find hidden treasures with sonar!\n\n"
        f"🎯 Scanning...\n"
        f"🔍 Nothing found this time!\n\n"
        f"Try again later!"
    )

# ==================== MODULE 10: STATISTICS COMMANDS ====================

async def moneyboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /mb command (Money Leaderboard)"""
    session = get_db()
    try:
        # Get top 10 users by balance
        top_users = session.query(User).order_by(User.balance.desc()).limit(10).all()
        
        text = "💰 *RICHEST PLAYERS*\n═══════════════════\n\n"
        
        medals = ["🥇", "🥈", "🥉"]
        for i, user in enumerate(top_users, 1):
            medal = medals[i-1] if i <= 3 else f"{i}."
            text += f"{medal} @{user.username or 'Unknown'} - {format_money(user.balance)}\n"
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    finally:
        session.close()

async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /leaderboard command (Family Leaderboard)"""
    session = get_db()
    try:
        # Get users by family size
        from sqlalchemy import func
        family_sizes = session.query(
            FamilyMember.parent_id,
            func.count(FamilyMember.id).label('count')
        ).group_by(FamilyMember.parent_id).order_by(func.count(FamilyMember.id).desc()).limit(10).all()
        
        text = "👨‍👩‍👧 *FAMILY LEADERBOARD*\n═══════════════════\n\n"
        
        medals = ["🥇", "🥈", "🥉"]
        for i, (parent_id, count) in enumerate(family_sizes, 1):
            user = session.query(User).filter_by(telegram_id=parent_id).first()
            medal = medals[i-1] if i <= 3 else f"{i}."
            text += f"{medal} @{user.username if user else 'Unknown'} - {count} children\n"
        
        if not family_sizes:
            text += "(No families yet)\n"
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    finally:
        session.close()

async def showstats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /showstats command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        # Get stats
        children_count = session.query(FamilyMember).filter_by(parent_id=user.telegram_id).count()
        partners_count = session.query(Partnership).filter(
            ((Partnership.user1_id == user.telegram_id) | (Partnership.user2_id == user.telegram_id)),
            Partnership.is_active == True
        ).count()
        friends_count = session.query(Friendship).filter(
            ((Friendship.user1_id == user.telegram_id) | (Friendship.user2_id == user.telegram_id)),
            Friendship.status == 'accepted'
        ).count()
        
        text = f"""
📊 *YOUR STATISTICS*
═══════════════════

👨‍👩‍👧 *Family:*
  Children: {children_count}
  Partners: {partners_count}

👥 *Social:*
  Friends: {friends_count}/{LIMITS['max_friends']}

💰 *Economy:*
  Balance: {format_money(user.balance)}
  Bank: {format_money(user.bank_balance)}
  Reputation: {user.reputation}

⚔️ *Combat:*
  Weapon: {user.current_weapon.title()}
  Health: {user.health}/{user.max_health}
  Kills Today: {user.kill_count_today}/{LIMITS['max_kills_per_day']}
  Robberies Today: {user.robbery_count_today}/{LIMITS['max_robbery_per_day']}

📅 *Account:*
  Created: {user.created_at.strftime('%Y-%m-%d')}
  Daily Streak: {user.daily_streak} days
        """
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    finally:
        session.close()

async def interactions_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /interactions command"""
    await update.message.reply_text(
        f"🤝 *YOUR INTERACTIONS*\n"
        f"═══════════════════\n\n"
        f"📊 Interaction statistics coming soon!\n\n"
        f"Track who you interact with most!"
    )
