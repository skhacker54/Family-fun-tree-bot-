"""
Message Handlers for Fam Tree Bot
==================================
Handle text messages and game answers
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from datetime import datetime, timedelta

from models.database import *
from config.settings import *
from utils.helpers import *
from handlers.commands import get_db, get_or_create_user
from handlers.commands3 import active_games

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages - check for game answers"""
    if not update.message or not update.message.text:
        return
    
    text = update.message.text.strip().upper()
    user_id = update.effective_user.id
    
    # Check if user is playing a game
    if user_id in active_games:
        game = active_games[user_id]
        game_type = game.get('game')
        
        # Check timeout
        if 'start_time' in game:
            elapsed = (datetime.utcnow() - game['start_time']).total_seconds()
            timeout = 300  # 5 minutes default
            if elapsed > timeout:
                del active_games[user_id]
                return
        
        session = get_db()
        try:
            user = get_or_create_user(update.effective_user, session)
            
            if game_type == '4pics':
                # 4 Pics 1 Word answer
                correct_word = game.get('word', '')
                if text == correct_word:
                    reward = 50
                    user.balance += reward
                    user.reputation += 3
                    session.commit()
                    await update.message.reply_text(
                        f"🎉 *CORRECT!*\n\n"
                        f"The word was: {correct_word}\n"
                        f"💰 You won ${reward}!\n"
                        f"⭐ Reputation +3",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    del active_games[user_id]
                else:
                    await update.message.reply_text("❌ Wrong! Try again!")
            
            elif game_type == 'nation':
                # Nation guessing answer
                correct_country = game.get('answer', '')
                if text.lower() == correct_country.lower():
                    reward = 100
                    user.balance += reward
                    user.reputation += 5
                    session.commit()
                    await update.message.reply_text(
                        f"🎉 *CORRECT!*\n\n"
                        f"The country was: {correct_country.title()}\n"
                        f"💰 You won ${reward}!\n"
                        f"⭐ Reputation +5",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    del active_games[user_id]
                else:
                    await update.message.reply_text("❌ Wrong! Try again!")
            
            elif game_type == 'ftrivia':
                # Family trivia answer
                correct_answer = game.get('answer', '')
                if text.lower() in correct_answer.lower():
                    reward = 30
                    user.balance += reward
                    user.reputation += 2
                    session.commit()
                    await update.message.reply_text(
                        f"🎉 *CORRECT!*\n\n"
                        f"💰 You won ${reward}!\n"
                        f"⭐ Reputation +2",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    del active_games[user_id]
                else:
                    await update.message.reply_text("❌ Wrong! Try again!")
        
        finally:
            session.close()
    
    # Check for natural language commands
    text_lower = update.message.text.lower()
    
    if "adopt" in text_lower and update.message.reply_to_message:
        from handlers.commands import adopt_command
        await adopt_command(update, context)
    elif "marry" in text_lower and update.message.reply_to_message:
        from handlers.commands import marry_command
        await marry_command(update, context)
    elif text_lower in ["tree", "family tree", "my tree"]:
        from handlers.commands import tree_command
        await tree_command(update, context)
    elif text_lower in ["account", "profile", "me", "my account"]:
        from handlers.commands import account_command
        await account_command(update, context)
    elif text_lower in ["daily", "bonus", "claim"]:
        from handlers.commands2 import daily_command
        await daily_command(update, context)
    elif text_lower in ["garden", "my garden"]:
        from handlers.commands2 import garden_command
        await garden_command(update, context)
    elif text_lower in ["help", "commands", "?"]:
        from handlers.commands import help_command
        await help_command(update, context)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo uploads"""
    if update.message.caption and update.message.caption.startswith('/setpic'):
        session = get_db()
        try:
            user = get_or_create_user(update.effective_user, session)
            
            # Get the largest photo
            photo = update.message.photo[-1]
            user.profile_pic = photo.file_id
            session.commit()
            
            await update.message.reply_text("✅ Profile picture updated!")
        finally:
            session.close()

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle sticker uploads"""
    if update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
        # Could be setting a custom GIF
        pass

async def handle_inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline queries"""
    query = update.inline_query.query
    
    if not query:
        return
    
    results = []
    
    # Search for users
    session = get_db()
    try:
        users = session.query(User).filter(
            User.username.ilike(f"%{query}%")
        ).limit(5).all()
        
        for user in users:
            results.append(
                InlineQueryResultArticle(
                    id=str(user.telegram_id),
                    title=f"@{user.username or 'Unknown'}",
                    description=f"Reputation: {user.reputation} | Balance: {format_money(user.balance)}",
                    input_message_content=InputTextMessageContent(
                        f"👤 User: @{user.username or 'Unknown'}\n"
                        f"⭐ Reputation: {user.reputation}\n"
                        f"💰 Balance: {format_money(user.balance)}"
                    ),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("➕ Add Friend", callback_data=f"friend_add_{user.telegram_id}")]
                    ])
                )
            )
    finally:
        session.close()
    
    await update.inline_query.answer(results, cache_time=1)

# Import needed for inline query
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
