"""
Utility, Settings, and Extra Features Commands
===============================================
All utility, settings, and extra feature commands
"""

import random
import aiohttp
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from models.database import *
from config.settings import *
from utils.helpers import *
from utils.keyboards import *
from handlers.commands import get_db, get_or_create_user

# ==================== MODULE 11: UTILITY COMMANDS ====================

async def figlet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /figlet command"""
    if not context.args:
        await update.message.reply_text("❌ Usage: /figlet [text]")
        return
    
    text = ' '.join(context.args)
    # Simple ASCII art
    ascii_art = f"""
╔{'═' * (len(text) + 2)}╗
║ {text.upper()} ║
╚{'═' * (len(text) + 2)}╝
    """
    await update.message.reply_text(f"<pre>{ascii_art}</pre>", parse_mode=ParseMode.HTML)

async def qotd_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /qotd command"""
    quote = get_quote_of_the_day()
    await update.message.reply_text(f"📜 *Quote of the Day*\n\n{quote}", parse_mode=ParseMode.MARKDOWN)

async def shibapic_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /shibapic command"""
    await update.message.reply_text(
        "🐕 *Random Shiba Inu*\n\n"
        "[Click here for a cute Shiba!](https://shiba.online/api/shibes)",
        parse_mode=ParseMode.MARKDOWN
    )

async def foodpic_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /foodpic command"""
    foods = ["🍕 Pizza", "🍔 Burger", "🍣 Sushi", "🍜 Ramen", "🥗 Salad", "🍰 Cake", "🍦 Ice Cream"]
    food = random.choice(foods)
    await update.message.reply_text(f"🍽️ *Random Food*\n\nHow about some {food}?")

async def randomjoke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /randomjoke command"""
    joke = get_random_joke()
    await update.message.reply_text(f"😄 *Random Joke*\n\n{joke}")

async def dadjoke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /dadjoke command"""
    joke = get_dad_joke()
    await update.message.reply_text(f"👨 *Dad Joke*\n\n{joke}")

async def evilinsult_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /evilinsult command"""
    insult = get_evil_insult()
    await update.message.reply_text(f"😈 *Playful Insult*\n\n{insult}")

async def randomadvice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /randomadvice command"""
    advice = get_random_advice()
    await update.message.reply_text(f"💡 *Life Advice*\n\n{advice}")

async def shorten_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /shorten command"""
    if not context.args:
        await update.message.reply_text("❌ Usage: /shorten [url]")
        return
    
    url = context.args[0]
    await update.message.reply_text(
        f"🔗 *URL Shortener*\n\n"
        f"Original: {url}\n"
        f"Shortened: [Click here]({url})\n\n"
        f"_(Note: This is a demo - integrate with a URL shortener API for real functionality)_",
        parse_mode=ParseMode.MARKDOWN
    )

async def name2gender_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /name2gender command"""
    if not context.args:
        await update.message.reply_text("❌ Usage: /name2gender [name]")
        return
    
    name = context.args[0]
    # Simple heuristic
    female_names = ['anna', 'maria', 'sarah', 'jessica', 'emma', 'olivia', 'sophia', 'mia']
    is_female = name.lower() in female_names
    
    gender = "Female 👩" if is_female else "Male 👨 (probably)"
    await update.message.reply_text(f"📝 *Gender Prediction*\n\nName: {name.title()}\nGender: {gender}")

async def name2nation_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /name2nation command"""
    if not context.args:
        await update.message.reply_text("❌ Usage: /name2nation [name]")
        return
    
    name = context.args[0]
    nations = ["🇺🇸 United States", "🇬🇧 United Kingdom", "🇩🇪 Germany", "🇫🇷 France", "🇮🇹 Italy", "🇪🇸 Spain", "🇯🇵 Japan"]
    nation = random.choice(nations)
    
    await update.message.reply_text(f"🌍 *Nationality Prediction*\n\nName: {name.title()}\nLikely from: {nation}")

async def ip2loc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ip2loc command"""
    if not context.args:
        await update.message.reply_text("❌ Usage: /ip2loc [ip_address]")
        return
    
    ip = context.args[0]
    await update.message.reply_text(
        f"📍 *IP Geolocation*\n\n"
        f"IP: {ip}\n"
        f"Country: United States 🇺🇸\n"
        f"City: New York\n"
        f"ISP: Example ISP\n\n"
        f"_(Note: This is a demo - integrate with an IP geolocation API for real functionality)_"
    )

# ==================== MODULE 12: SETTINGS COMMANDS ====================

async def setlang_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /setlang command"""
    await update.message.reply_text(
        "🌐 *SELECT LANGUAGE*\n═══════════════════",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_language_keyboard()
    )

async def scope_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /scope command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        current_scope = user.settings.get('tree_scope', 'group')
        
        keyboard = [
            [InlineKeyboardButton(
                f"{'✅ ' if current_scope == 'group' else ''}Group Only", 
                callback_data="scope_group"
            )],
            [InlineKeyboardButton(
                f"{'✅ ' if current_scope == 'global' else ''}Global", 
                callback_data="scope_global"
            )],
            [InlineKeyboardButton("🔙 Back", callback_data="settings_menu")],
        ]
        
        await update.message.reply_text(
            "🌳 *TREE SCOPE SETTINGS*\n═══════════════════\n\n"
            "Select who can see your family tree:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    finally:
        session.close()

async def toggle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /toggle command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        settings = user.settings or {}
        
        keyboard = [
            [InlineKeyboardButton(
                f"{'✅ ' if settings.get('garden_enabled', True) else '❌ '}Garden", 
                callback_data="toggle_garden"
            )],
            [InlineKeyboardButton(
                f"{'✅ ' if settings.get('games_enabled', True) else '❌ '}Games", 
                callback_data="toggle_games"
            )],
            [InlineKeyboardButton(
                f"{'✅ ' if settings.get('robkill_enabled', True) else '❌ '}Rob/Kill", 
                callback_data="toggle_robkill"
            )],
            [InlineKeyboardButton(
                f"{'✅ ' if settings.get('notifications', True) else '❌ '}Notifications", 
                callback_data="toggle_notifications"
            )],
            [InlineKeyboardButton("🔙 Back", callback_data="settings_menu")],
        ]
        
        await update.message.reply_text(
            "⚙️ *TOGGLE FEATURES*\n═══════════════════\n\n"
            "Click to enable/disable features:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    finally:
        session.close()

async def autoprune_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /autoprune command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        settings = user.settings or {}
        current = settings.get('auto_prune', 3600)  # Default 1 hour
        
        keyboard = [
            [InlineKeyboardButton("30 minutes", callback_data="prune_1800")],
            [InlineKeyboardButton("1 hour", callback_data="prune_3600")],
            [InlineKeyboardButton("6 hours", callback_data="prune_21600")],
            [InlineKeyboardButton("24 hours", callback_data="prune_86400")],
            [InlineKeyboardButton("🔙 Back", callback_data="settings_menu")],
        ]
        
        await update.message.reply_text(
            "🗑️ *AUTO PRUNE SETTINGS*\n═══════════════════\n\n"
            f"Current: {format_time(current)}\n\n"
            "Select auto-delete duration:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    finally:
        session.close()

async def prune_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /prune command"""
    await update.message.reply_text(
        "🗑️ *MANUAL PRUNE*\n═══════════════════\n\n"
        "This would delete bot messages in this chat.\n"
        "_(Admin only feature)_"
    )

# ==================== MODULE 13: EXTRA FEATURES ====================

async def waifu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /waifu command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        # Get friends
        friendships = session.query(Friendship).filter(
            ((Friendship.user1_id == user.telegram_id) | (Friendship.user2_id == user.telegram_id)),
            Friendship.status == 'accepted'
        ).all()
        
        if not friendships:
            await update.message.reply_text("❌ You need friends first! Use /friend to add friends.")
            return
        
        # Select random friend as waifu
        friendship = random.choice(friendships)
        waifu_id = friendship.user2_id if friendship.user1_id == user.telegram_id else friendship.user1_id
        waifu = session.query(User).filter_by(telegram_id=waifu_id).first()
        
        if waifu:
            await update.message.reply_text(
                f"💕 *YOUR DAILY WAIFU*\n"
                f"═══════════════════\n\n"
                f"Today's special person:\n"
                f"@{waifu.username or 'Unknown'}\n\n"
                f"💝 Treat them well!"
            )
        else:
            await update.message.reply_text("❌ Could not find waifu!")
    finally:
        session.close()

async def waifus_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /waifus command"""
    await update.message.reply_text(
        "💕 *GROUP WAIFUS*\n═══════════════════\n\n"
        "View all members' daily waifus!\n\n"
        "_(Feature coming soon)_"
    )

async def setloc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /setloc command"""
    if not context.args:
        await update.message.reply_text(
            "❌ Usage: /setloc [location]\n"
            "Examples:\n"
            "/setloc New York\n"
            "/setloc Tokyo\n"
            "/setloc Paris"
        )
        return
    
    location = ' '.join(context.args)
    
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        settings = user.settings or {}
        settings['location'] = location
        user.settings = settings
        session.commit()
        
        await update.message.reply_text(
            f"📍 *LOCATION SET*\n\n"
            f"Your location: {location}\n\n"
            f"Use /showmap to see family locations!"
        )
    finally:
        session.close()

async def showmap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /showmap command"""
    await update.message.reply_text(
        "🗺️ *FAMILY MAP*\n═══════════════════\n\n"
        "World map with family pins:\n\n"
        "🇺🇸 @User1 - New York\n"
        "🇯🇵 @User2 - Tokyo\n"
        "🇬🇧 @User3 - London\n\n"
        "_(Interactive map coming soon)_"
    )

async def wedcard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /wedcard command"""
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to your partner!")
        return
    
    partner = update.message.reply_to_message.from_user
    user = update.effective_user
    
    card = f"""
💌💌💌💌💌💌💌💌💌💌💌💌💌💌💌💌💌
💌                                    💌
💌      💍 WEDDING INVITATION 💍      💌
💌                                    💌
💌   We joyfully invite you to        💌
💌   celebrate the marriage of:       💌
💌                                    💌
💌        @{user.username or 'Bride'}  💌
💌              &                     💌
💌     @{partner.username or 'Groom'} 💌
💌                                    💌
💌   💕 Join us in this celebration! 💕💌
💌                                    💌
💌💌💌💌💌💌💌💌💌💌💌💌💌💌💌💌💌
    """
    
    await update.message.reply_text(card)

async def refer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /refer command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        referral_link = f"https://t.me/{BOT_NAME_BETA.replace('@', '')}?start={user.referral_code}"
        
        await update.message.reply_text(
            f"🎁 *REFERRAL PROGRAM*\n"
            f"═══════════════════\n\n"
            f"Your referral link:\n"
            f"`{referral_link}`\n\n"
            f"💰 Rewards:\n"
            f"  • You: ${REFERRAL_REWARDS['referrer']:,}\n"
            f"  • Friend: ${REFERRAL_REWARDS['referred']:,}\n\n"
            f"📊 Your referrals: {user.referral_count}\n\n"
            f"Share this link with friends!",
            parse_mode=ParseMode.MARKDOWN
        )
    finally:
        session.close()

async def block_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /block command"""
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to the user you want to block!")
        return
    
    target_user = update.message.reply_to_message.from_user
    
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        # Check if already blocked
        existing = session.query(BlockedUser).filter_by(
            blocker_id=user.telegram_id, blocked_id=target_user.id
        ).first()
        
        if existing:
            await update.message.reply_text("❌ User is already blocked!")
            return
        
        block = BlockedUser(blocker_id=user.telegram_id, blocked_id=target_user.id)
        session.add(block)
        session.commit()
        
        await update.message.reply_text(
            f"🚫 *USER BLOCKED*\n\n"
            f"@{target_user.username or 'Unknown'} can no longer:\n"
            f"  • Send you adoption requests\n"
            f"  • Send you marriage proposals\n"
            f"  • Add you as a friend"
        )
    finally:
        session.close()

async def unblock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /unblock command"""
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to the user you want to unblock!")
        return
    
    target_user = update.message.reply_to_message.from_user
    
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        block = session.query(BlockedUser).filter_by(
            blocker_id=user.telegram_id, blocked_id=target_user.id
        ).first()
        
        if not block:
            await update.message.reply_text("❌ User is not blocked!")
            return
        
        session.delete(block)
        session.commit()
        
        await update.message.reply_text(
            f"✅ *USER UNBLOCKED*\n\n"
            f"@{target_user.username or 'Unknown'} has been unblocked."
        )
    finally:
        session.close()

async def blocklist_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /blocklist command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        blocks = session.query(BlockedUser).filter_by(blocker_id=user.telegram_id).all()
        
        text = "🚫 *BLOCKED USERS*\n═══════════════════\n\n"
        
        if blocks:
            for block in blocks:
                blocked_user = session.query(User).filter_by(telegram_id=block.blocked_id).first()
                if blocked_user:
                    text += f"• @{blocked_user.username or 'Unknown'}\n"
        else:
            text += "(No blocked users)"
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    finally:
        session.close()
