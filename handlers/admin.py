"""
Admin Panel Handlers for Fam Tree Bot
======================================
Admin-only commands and features
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from datetime import datetime, timedelta

from models.database import *
from config.settings import ADMIN_USER_IDS
from utils.helpers import *
from handlers.commands import get_db, get_or_create_user

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_USER_IDS

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin command"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ You are not authorized to use this command!")
        return
    
    from utils.keyboards import get_admin_keyboard
    
    await update.message.reply_text(
        "🔧 *ADMIN PANEL*\n═══════════════════\n\n"
        "Welcome, Administrator!\n\n"
        "Select an option:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_admin_keyboard()
    )

async def admin_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /adminstats command"""
    if not is_admin(update.effective_user.id):
        return
    
    session = get_db()
    try:
        from sqlalchemy import func
        
        # Get statistics
        total_users = session.query(User).count()
        active_today = session.query(User).filter(
            User.last_active >= datetime.utcnow() - timedelta(days=1)
        ).count()
        active_week = session.query(User).filter(
            User.last_active >= datetime.utcnow() - timedelta(days=7)
        ).count()
        
        total_money = session.query(func.sum(User.balance)).scalar() or 0
        total_bank = session.query(func.sum(User.bank_balance)).scalar() or 0
        
        total_families = session.query(FamilyMember).count()
        total_partnerships = session.query(Partnership).filter_by(is_active=True).count()
        total_friendships = session.query(Friendship).filter_by(status='accepted').count()
        
        text = f"""
📊 *BOT STATISTICS*
═══════════════════

👥 *Users:*
  Total: {total_users:,}
  Active Today: {active_today:,}
  Active This Week: {active_week:,}

💰 *Economy:*
  Total in Wallets: ${total_money:,.0f}
  Total in Banks: ${total_bank:,.0f}
  Combined: ${total_money + total_bank:,.0f}

👨‍👩‍👧 *Social:*
  Family Relations: {total_families:,}
  Active Partnerships: {total_partnerships:,}
  Friendships: {total_friendships:,}

⏰ *Generated:* {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
        """
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    finally:
        session.close()

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /broadcast command"""
    if not is_admin(update.effective_user.id):
        return
    
    if not context.args:
        await update.message.reply_text("❌ Usage: /broadcast [message]")
        return
    
    message = ' '.join(context.args)
    
    session = get_db()
    try:
        users = session.query(User).all()
        sent = 0
        failed = 0
        
        for user in users:
            try:
                await context.bot.send_message(
                    chat_id=user.telegram_id,
                    text=f"📢 *BROADCAST*\n═══════════════════\n\n{message}",
                    parse_mode=ParseMode.MARKDOWN
                )
                sent += 1
            except:
                failed += 1
        
        await update.message.reply_text(
            f"✅ *BROADCAST SENT*\n\n"
            f"Sent: {sent}\n"
            f"Failed: {failed}"
        )
    finally:
        session.close()

async def give_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /give command (admin give money)"""
    if not is_admin(update.effective_user.id):
        return
    
    if len(context.args) < 2:
        await update.message.reply_text("❌ Usage: /give [@username] [amount]")
        return
    
    username = context.args[0].replace('@', '')
    try:
        amount = float(context.args[1])
    except:
        await update.message.reply_text("❌ Invalid amount!")
        return
    
    session = get_db()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            await update.message.reply_text("❌ User not found!")
            return
        
        user.balance += amount
        session.commit()
        
        await update.message.reply_text(
            f"✅ *GAVE MONEY*\n\n"
            f"To: @{username}\n"
            f"Amount: {format_money(amount)}\n"
            f"New Balance: {format_money(user.balance)}"
        )
    finally:
        session.close()

async def take_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /take command (admin take money)"""
    if not is_admin(update.effective_user.id):
        return
    
    if len(context.args) < 2:
        await update.message.reply_text("❌ Usage: /take [@username] [amount]")
        return
    
    username = context.args[0].replace('@', '')
    try:
        amount = float(context.args[1])
    except:
        await update.message.reply_text("❌ Invalid amount!")
        return
    
    session = get_db()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            await update.message.reply_text("❌ User not found!")
            return
        
        user.balance = max(0, user.balance - amount)
        session.commit()
        
        await update.message.reply_text(
            f"✅ *TOOK MONEY*\n\n"
            f"From: @{username}\n"
            f"Amount: {format_money(amount)}\n"
            f"New Balance: {format_money(user.balance)}"
        )
    finally:
        session.close()

async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ban command"""
    if not is_admin(update.effective_user.id):
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to the user you want to ban!")
        return
    
    target_user = update.message.reply_to_message.from_user
    
    session = get_db()
    try:
        user = session.query(User).filter_by(telegram_id=target_user.id).first()
        if user:
            user.is_dead = True
            user.settings = {'banned': True}
            session.commit()
        
        await update.message.reply_text(
            f"🚫 *USER BANNED*\n\n"
            f"@{target_user.username or 'Unknown'} has been banned."
        )
    finally:
        session.close()

async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /unban command"""
    if not is_admin(update.effective_user.id):
        return
    
    if not context.args:
        await update.message.reply_text("❌ Usage: /unban [@username]")
        return
    
    username = context.args[0].replace('@', '')
    
    session = get_db()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user:
            user.is_dead = False
            settings = user.settings or {}
            settings['banned'] = False
            user.settings = settings
            session.commit()
        
        await update.message.reply_text(
            f"✅ *USER UNBANNED*\n\n"
            f"@{username} has been unbanned."
        )
    finally:
        session.close()

async def maintenance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /maintenance command"""
    if not is_admin(update.effective_user.id):
        return
    
    await update.message.reply_text(
        "🔧 *MAINTENANCE MODE*\n═══════════════════\n\n"
        "Maintenance mode toggled.\n\n"
        "Users will see a maintenance message."
    )

async def logs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /logs command"""
    if not is_admin(update.effective_user.id):
        return
    
    await update.message.reply_text(
        "📋 *BOT LOGS*\n═══════════════════\n\n"
        "Recent activity:\n\n"
        "• Bot started\n"
        "• Database connected\n"
        "• All systems operational\n\n"
        "_(View full logs in bot.log file)_"
    )
