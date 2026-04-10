"""
Command Handlers for Fam Tree Bot
==================================
All 200+ command handlers organized by module
"""

import logging
import random
from datetime import datetime, timedelta
from typing import Optional

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from models.database import User, FamilyMember, Partnership, Friendship, Worker, GardenPlot, BarnItem, Insurance, MarketListing, Achievement, Transaction, CustomGIF, get_session, init_db
from config.settings import *
from utils.helpers import *
from utils.keyboards import *

logger = logging.getLogger(__name__)

# Initialize database
engine = init_db()

def get_db():
    """Get database session"""
    return get_session(engine)

def get_or_create_user(telegram_user, session) -> User:
    """Get or create user from Telegram user"""
    user = session.query(User).filter_by(telegram_id=telegram_user.id).first()
    if not user:
        user = User(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            language_code=telegram_user.language_code or 'en',
            referral_code=generate_referral_code(telegram_user.id)
        )
        # Initialize garden plots
        for i in range(9):
            plot = GardenPlot(owner_id=telegram_user.id, plot_number=i+1, is_empty=True)
            session.add(plot)
        session.add(user)
        session.commit()
    return user

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    session = get_db()
    try:
        telegram_user = update.effective_user
        user = get_or_create_user(telegram_user, session)
        
        # Check for referral
        if context.args and context.args[0].startswith('ref_'):
            ref_code = context.args[0]
            referrer = session.query(User).filter_by(referral_code=ref_code).first()
            if referrer and referrer.telegram_id != user.telegram_id:
                user.referred_by = referrer.telegram_id
                user.balance += REFERRAL_REWARDS['referred']
                referrer.balance += REFERRAL_REWARDS['referrer']
                referrer.referral_count += 1
                session.commit()
                await update.message.reply_text(
                    f"🎉 Welcome! You received ${REFERRAL_REWARDS['referred']:,} bonus!\n"
                    f"Your referrer received ${REFERRAL_REWARDS['referrer']:,}!"
                )
        
        welcome_text = f"""
🌳 *Welcome to Fam Tree Bot!*

Your ultimate family simulation RPG experience!

*What you can do:*
🌳 Build your family tree
👥 Make friends worldwide
💰 Earn and trade money
🌱 Grow your garden
🏭 Manage workers
🎮 Play mini-games
⚔️ PvP combat

*Get started:*
Use the menu below or type /help for all commands!

💰 Starting balance: ${STARTING_BALANCE:,}
        """
        
        await update.message.reply_text(
            welcome_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_main_menu_keyboard()
        )
    finally:
        session.close()

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
🌳 *FAM TREE BOT - COMMAND GUIDE*
═══════════════════════════════

*👨‍👩‍👧 FAMILY COMMANDS:*
/tree - View your family tree
/adopt - Adopt a user (reply)
/marry - Propose marriage (reply)
/divorce - Divorce partner
/disown - Remove adopted child
/runaway - Leave your family
/relations - View close family
/fulltree - Extended family tree
/bloodtree - Blood relations only

*👥 FRIEND COMMANDS:*
/friend - Send friend request (reply)
/unfriend - Remove friend
/circle - View friend network
/suggestions - Friend recommendations
/flink - Get friend link
/activefriends - Online friends

*💰 ACCOUNT COMMANDS:*
/account - Your profile
/bank - Bank operations
/pay [amount] - Transfer money
/weapon - Select weapon
/rob - Rob a user (reply)
/kill - Kill a user (reply)
/insurance - Manage insurance

*🌱 GARDEN COMMANDS:*
/garden - View your garden
/plant [crop] - Plant crops
/harvest - Harvest ready crops
/barn - View barn contents
/orders - View orders
/stands - Global marketplace

*🏭 FACTORY COMMANDS:*
/factory - Factory dashboard
/hire - Hire worker (reply)
/buy shield - Buy protection
/buy sword - Break shields

*🎮 GAME COMMANDS:*
/daily - Claim daily reward
/fuse - Fuse gemstones
/4p - 4 Pics 1 Word
/ripple - Ripple betting
/nation - Nation guessing
/lottery - Lottery

*📊 STAT COMMANDS:*
/mb - Money leaderboard
/leaderboard - Family rankings
/showstats - Your statistics

*⚙️ SETTINGS:*
/setlang - Change language
/scope - Tree scope settings
/toggle - Toggle features

Type any command to get started!
    """
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

# ==================== MODULE 1: FAMILY COMMANDS ====================

async def tree_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /tree command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        # Get family members
        children = session.query(FamilyMember).filter_by(parent_id=user.telegram_id).all()
        partnerships = session.query(Partnership).filter(
            ((Partnership.user1_id == user.telegram_id) | (Partnership.user2_id == user.telegram_id)),
            Partnership.is_active == True
        ).all()
        
        tree_text = f"""
🌳 *YOUR FAMILY TREE*
═══════════════════

👤 *You:* @{user.username or 'Unknown'}

💍 *Partners:*
"""
        if partnerships:
            for p in partnerships:
                partner_id = p.user2_id if p.user1_id == user.telegram_id else p.user1_id
                partner = session.query(User).filter_by(telegram_id=partner_id).first()
                if partner:
                    tree_text += f"  💕 @{partner.username or 'Unknown'}\n"
        else:
            tree_text += "  (No partners)\n"
        
        tree_text += "\n👶 *Children:*\n"
        if children:
            for child in children:
                child_user = session.query(User).filter_by(telegram_id=child.user_id).first()
                if child_user:
                    tree_text += f"  👶 @{child_user.username or 'Unknown'}\n"
        else:
            tree_text += "  (No children)\n"
        
        tree_text += f"\n📊 Total Family: {len(children) + len(partnerships)} members"
        
        await update.message.reply_text(tree_text, parse_mode=ParseMode.MARKDOWN)
    finally:
        session.close()

async def adopt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /adopt command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to the user you want to adopt!")
            return
        
        target_user = update.message.reply_to_message.from_user
        if target_user.id == user.telegram_id:
            await update.message.reply_text("❌ You cannot adopt yourself!")
            return
        
        # Check if already adopted
        existing = session.query(FamilyMember).filter_by(
            user_id=target_user.id, parent_id=user.telegram_id
        ).first()
        if existing:
            await update.message.reply_text("❌ This user is already your child!")
            return
        
        # Check children limit
        children_count = session.query(FamilyMember).filter_by(parent_id=user.telegram_id).count()
        if children_count >= LIMITS['max_children']:
            await update.message.reply_text(f"❌ You already have {LIMITS['max_children']} children (max limit)!")
            return
        
        # Send adoption request
        await update.message.reply_text(
            f"🍼 *Adoption Request*\n\n"
            f"@{user.username} wants to adopt you!\n"
            f"Do you accept?",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_confirmation_keyboard(
                f"adopt_yes_{user.telegram_id}_{target_user.id}",
                f"adopt_no_{user.telegram_id}_{target_user.id}"
            )
        )
    finally:
        session.close()

async def marry_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /marry command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to the user you want to marry!")
            return
        
        target_user = update.message.reply_to_message.from_user
        if target_user.id == user.telegram_id:
            await update.message.reply_text("❌ You cannot marry yourself!")
            return
        
        # Check if already married to this person
        existing = session.query(Partnership).filter(
            ((Partnership.user1_id == user.telegram_id) & (Partnership.user2_id == target_user.id)) |
            ((Partnership.user1_id == target_user.id) & (Partnership.user2_id == user.telegram_id)),
            Partnership.is_active == True
        ).first()
        if existing:
            await update.message.reply_text("❌ You are already married to this person!")
            return
        
        # Check partners limit
        partners_count = session.query(Partnership).filter(
            (Partnership.user1_id == user.telegram_id) | (Partnership.user2_id == user.telegram_id),
            Partnership.is_active == True
        ).count()
        if partners_count >= LIMITS['max_partners']:
            await update.message.reply_text(f"❌ You already have {LIMITS['max_partners']} partners (max limit)!")
            return
        
        # Send marriage proposal
        await update.message.reply_text(
            f"💍 *Marriage Proposal*\n\n"
            f"@{user.username} wants to marry you!\n"
            f"Will you accept?",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_confirmation_keyboard(
                f"marry_yes_{user.telegram_id}_{target_user.id}",
                f"marry_no_{user.telegram_id}_{target_user.id}"
            )
        )
    finally:
        session.close()

async def divorce_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /divorce command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        # Get active partnerships
        partnerships = session.query(Partnership).filter(
            ((Partnership.user1_id == user.telegram_id) | (Partnership.user2_id == user.telegram_id)),
            Partnership.is_active == True
        ).all()
        
        if not partnerships:
            await update.message.reply_text("❌ You are not married!")
            return
        
        # Create partner selection keyboard
        keyboard = []
        for p in partnerships:
            partner_id = p.user2_id if p.user1_id == user.telegram_id else p.user1_id
            partner = session.query(User).filter_by(telegram_id=partner_id).first()
            if partner:
                keyboard.append([InlineKeyboardButton(
                    f"💔 Divorce @{partner.username or 'Unknown'}",
                    callback_data=f"divorce_confirm_{partner_id}"
                )])
        keyboard.append([InlineKeyboardButton("🔙 Cancel", callback_data="cancel")])
        
        await update.message.reply_text(
            "💔 *Divorce*\n\nSelect partner to divorce:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    finally:
        session.close()

async def relations_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /relations command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        # Get all family relations
        children = session.query(FamilyMember).filter_by(parent_id=user.telegram_id).all()
        parents = session.query(FamilyMember).filter_by(user_id=user.telegram_id).all()
        partnerships = session.query(Partnership).filter(
            ((Partnership.user1_id == user.telegram_id) | (Partnership.user2_id == user.telegram_id)),
            Partnership.is_active == True
        ).all()
        
        text = "👨‍👩‍👧 *YOUR CLOSE FAMILY*\n═══════════════════\n\n"
        
        text += "💍 *Partners:*\n"
        for p in partnerships:
            partner_id = p.user2_id if p.user1_id == user.telegram_id else p.user1_id
            partner = session.query(User).filter_by(telegram_id=partner_id).first()
            if partner:
                text += f"  💕 @{partner.username or 'Unknown'}\n"
        if not partnerships:
            text += "  (None)\n"
        
        text += "\n👶 *Children:*\n"
        for child in children:
            child_user = session.query(User).filter_by(telegram_id=child.user_id).first()
            if child_user:
                text += f"  👶 @{child_user.username or 'Unknown'}\n"
        if not children:
            text += "  (None)\n"
        
        text += "\n👨‍👩 *Parents:*\n"
        for parent in parents:
            parent_user = session.query(User).filter_by(telegram_id=parent.parent_id).first()
            if parent_user:
                text += f"  👨‍👩 @{parent_user.username or 'Unknown'}\n"
        if not parents:
            text += "  (None)\n"
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    finally:
        session.close()

# ==================== MODULE 2: FRIEND COMMANDS ====================

async def friend_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /friend command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to the user you want to add as friend!")
            return
        
        target_user = update.message.reply_to_message.from_user
        if target_user.id == user.telegram_id:
            await update.message.reply_text("❌ You cannot add yourself as friend!")
            return
        
        # Check if already friends
        existing = session.query(Friendship).filter(
            ((Friendship.user1_id == user.telegram_id) & (Friendship.user2_id == target_user.id)) |
            ((Friendship.user1_id == target_user.id) & (Friendship.user2_id == user.telegram_id)),
            Friendship.status == 'accepted'
        ).first()
        if existing:
            await update.message.reply_text("❌ You are already friends with this user!")
            return
        
        # Check pending request
        pending = session.query(Friendship).filter(
            Friendship.user1_id == user.telegram_id,
            Friendship.user2_id == target_user.id,
            Friendship.status == 'pending'
        ).first()
        if pending:
            await update.message.reply_text("❌ Friend request already sent!")
            return
        
        # Check friends limit
        friends_count = session.query(Friendship).filter(
            ((Friendship.user1_id == user.telegram_id) | (Friendship.user2_id == user.telegram_id)),
            Friendship.status == 'accepted'
        ).count()
        if friends_count >= LIMITS['max_friends']:
            await update.message.reply_text(f"❌ You already have {LIMITS['max_friends']} friends (max limit)!")
            return
        
        # Create friendship
        friendship = Friendship(
            user1_id=user.telegram_id,
            user2_id=target_user.id,
            status='pending'
        )
        session.add(friendship)
        session.commit()
        
        await update.message.reply_text(
            f"✅ Friend request sent to @{target_user.username or 'Unknown'}!\n\n"
            f"💰 Both will receive ${FRIEND_BONUS:,} when accepted!"
        )
    finally:
        session.close()

async def unfriend_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /unfriend command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to the user you want to unfriend!")
            return
        
        target_user = update.message.reply_to_message.from_user
        
        # Find friendship
        friendship = session.query(Friendship).filter(
            ((Friendship.user1_id == user.telegram_id) & (Friendship.user2_id == target_user.id)) |
            ((Friendship.user1_id == target_user.id) & (Friendship.user2_id == user.telegram_id)),
            Friendship.status == 'accepted'
        ).first()
        
        if not friendship:
            await update.message.reply_text("❌ You are not friends with this user!")
            return
        
        session.delete(friendship)
        session.commit()
        
        await update.message.reply_text(
            f"💔 Removed @{target_user.username or 'Unknown'} from friends!\n"
            f"💰 -${FRIEND_BONUS:,} from both accounts"
        )
    finally:
        session.close()

async def circle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /circle command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        # Get friends
        friendships = session.query(Friendship).filter(
            ((Friendship.user1_id == user.telegram_id) | (Friendship.user2_id == user.telegram_id)),
            Friendship.status == 'accepted'
        ).all()
        
        text = "🌐 *YOUR FRIEND CIRCLE*\n═══════════════════\n\n"
        
        if friendships:
            for friendship in friendships:
                friend_id = friendship.user2_id if friendship.user1_id == user.telegram_id else friendship.user1_id
                friend = session.query(User).filter_by(telegram_id=friend_id).first()
                if friend:
                    # Check if online (active in last 5 minutes)
                    is_online = (datetime.utcnow() - friend.last_active) < timedelta(minutes=5)
                    status = "🟢" if is_online else "⚫"
                    text += f"{status} @{friend.username or 'Unknown'}\n"
        else:
            text += "(No friends yet)\n\nUse /friend to add friends!"
        
        text += f"\n📊 Total Friends: {len(friendships)}/{LIMITS['max_friends']}"
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    finally:
        session.close()

async def activefriends_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /activefriends command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        # Get online friends (active in last 5 minutes)
        five_min_ago = datetime.utcnow() - timedelta(minutes=5)
        
        friendships = session.query(Friendship).filter(
            ((Friendship.user1_id == user.telegram_id) | (Friendship.user2_id == user.telegram_id)),
            Friendship.status == 'accepted'
        ).all()
        
        online_friends = []
        for friendship in friendships:
            friend_id = friendship.user2_id if friendship.user1_id == user.telegram_id else friendship.user1_id
            friend = session.query(User).filter_by(telegram_id=friend_id).first()
            if friend and friend.last_active > five_min_ago:
                online_friends.append(friend)
        
        text = "🟢 *ONLINE FRIENDS*\n═══════════════════\n\n"
        
        if online_friends:
            for friend in online_friends:
                text += f"🟢 @{friend.username or 'Unknown'}\n"
        else:
            text += "(No friends online)\n"
        
        text += f"\n📊 Online: {len(online_friends)}/{len(friendships)}"
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    finally:
        session.close()

# ==================== MODULE 3: ACCOUNT COMMANDS ====================

async def account_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /account command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        # Update last active
        user.last_active = datetime.utcnow()
        session.commit()
        
        # Get insurance count
        insurance_count = session.query(Insurance).filter_by(owner_id=user.telegram_id, is_active=True).count()
        
        # Get weapon name
        weapon_name = user.current_weapon.replace('_', ' ').title()
        
        # Create health bar
        health_bar = '❤️' * user.health + '🖤' * (user.max_health - user.health)
        
        text = f"""
┌─────────────────────────────────────────┐
│ 👤 *USER PROFILE*                       │
├─────────────────────────────────────────┤
│                                         │
│  @{user.username or 'Unknown'}          │
│                                         │
│  💰 *Balance:* {format_money(user.balance)}           │
│  🏦 *Bank:* {format_money(user.bank_balance)}             │
│  ⭐ *Reputation:* {user.reputation}/200          │
│  💼 *Job:* {user.job.title()}                 │
│                                         │
│  💎 *Gemstone:* {user.gemstone or 'None'}              │
│  🔫 *Weapon:* {weapon_name}              │
│  🛡️ *Insurance:* {insurance_count} Active              │
│  ❤️ *Health:* {health_bar}        │
│                                         │
└─────────────────────────────────────────┘
        """
        
        await update.message.reply_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_account_keyboard()
        )
    finally:
        session.close()

async def bank_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /bank command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        text = f"""
🏦 *BANK ACCOUNT*
═══════════════════

💰 Wallet: {format_money(user.balance)}
🏦 Bank: {format_money(user.bank_balance)}
💵 Total: {format_money(user.balance + user.bank_balance)}

Use buttons below to manage:
        """
        
        await update.message.reply_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_bank_keyboard()
        )
    finally:
        session.close()

async def deposit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /deposit command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not context.args:
            await update.message.reply_text(
                "❌ Usage: /deposit [amount]\n"
                "Examples:\n"
                "/deposit 1000\n"
                "/deposit all\n"
                "/deposit half"
            )
            return
        
        amount = parse_amount_expression(context.args[0], user.balance)
        
        if amount <= 0:
            await update.message.reply_text("❌ Invalid amount!")
            return
        
        if amount > user.balance:
            await update.message.reply_text("❌ Insufficient funds!")
            return
        
        user.balance -= amount
        user.bank_balance += amount
        session.commit()
        
        await update.message.reply_text(
            f"✅ Deposited {format_money(amount)} to bank!\n\n"
            f"💰 Wallet: {format_money(user.balance)}\n"
            f"🏦 Bank: {format_money(user.bank_balance)}"
        )
    finally:
        session.close()

async def withdraw_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /withdraw command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not context.args:
            await update.message.reply_text(
                "❌ Usage: /withdraw [amount]\n"
                "Examples:\n"
                "/withdraw 1000\n"
                "/withdraw all\n"
                "/withdraw half"
            )
            return
        
        amount = parse_amount_expression(context.args[0], user.bank_balance)
        
        if amount <= 0:
            await update.message.reply_text("❌ Invalid amount!")
            return
        
        if amount > user.bank_balance:
            await update.message.reply_text("❌ Insufficient bank balance!")
            return
        
        user.bank_balance -= amount
        user.balance += amount
        session.commit()
        
        await update.message.reply_text(
            f"✅ Withdrew {format_money(amount)} from bank!\n\n"
            f"💰 Wallet: {format_money(user.balance)}\n"
            f"🏦 Bank: {format_money(user.bank_balance)}"
        )
    finally:
        session.close()

async def pay_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pay command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to the user you want to pay!")
            return
        
        if not context.args:
            await update.message.reply_text("❌ Usage: /pay [amount]")
            return
        
        target_user = update.message.reply_to_message.from_user
        amount = parse_amount_expression(context.args[0], user.balance)
        
        if amount <= 0:
            await update.message.reply_text("❌ Invalid amount!")
            return
        
        if amount > user.balance:
            await update.message.reply_text("❌ Insufficient funds!")
            return
        
        # Get or create target user
        target = session.query(User).filter_by(telegram_id=target_user.id).first()
        if not target:
            await update.message.reply_text("❌ Target user not found!")
            return
        
        user.balance -= amount
        target.balance += amount
        
        # Record transaction
        transaction = Transaction(
            from_user_id=user.telegram_id,
            to_user_id=target.telegram_id,
            amount=amount,
            transaction_type='transfer',
            description=f'Payment from @{user.username} to @{target.username}'
        )
        session.add(transaction)
        session.commit()
        
        await update.message.reply_text(
            f"✅ Paid {format_money(amount)} to @{target.username or 'Unknown'}!\n\n"
            f"💰 Your balance: {format_money(user.balance)}"
        )
    finally:
        session.close()

async def weapon_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /weapon command"""
    await update.message.reply_text(
        "🔫 *WEAPON ARSENAL*\n"
        "═══════════════════\n\n"
        "Select your weapon:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_weapons_keyboard()
    )

async def rob_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /rob command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to the user you want to rob!")
            return
        
        target_user = update.message.reply_to_message.from_user
        if target_user.id == user.telegram_id:
            await update.message.reply_text("❌ You cannot rob yourself!")
            return
        
        # Check if dead
        if user.is_dead:
            await update.message.reply_text("❌ You cannot rob while dead! Use /medical to revive ($500)")
            return
        
        # Check daily limit
        if is_new_day(user.last_reset_day):
            user.robbery_count_today = 0
            user.last_reset_day = datetime.utcnow()
        
        if user.robbery_count_today >= LIMITS['max_robbery_per_day']:
            await update.message.reply_text(f"❌ You've reached your daily robbery limit ({LIMITS['max_robbery_per_day']}/day)!")
            return
        
        # Get target
        target = session.query(User).filter_by(telegram_id=target_user.id).first()
        if not target:
            await update.message.reply_text("❌ Target user not found!")
            return
        
        if target.balance <= 0:
            await update.message.reply_text("❌ This person has no money to rob!")
            return
        
        # Calculate success chance based on weapon
        weapon_power = WEAPONS.get(user.current_weapon, {}).get('rob_power', 50)
        success_chance = min(weapon_power / 2, 90)  # Max 90% success
        
        if random.random() * 100 < success_chance:
            # Success
            amount = calculate_rob_amount(target.balance, target.balance > 10000)
            amount = min(amount, target.balance)
            
            user.balance += amount
            target.balance -= amount
            user.robbery_count_today += 1
            user.reputation += 1
            
            # Record transaction
            transaction = Transaction(
                from_user_id=target.telegram_id,
                to_user_id=user.telegram_id,
                amount=amount,
                transaction_type='rob',
                description=f'Robbery by @{user.username}'
            )
            session.add(transaction)
            session.commit()
            
            await update.message.reply_text(
                f"🦹 *ROBBERY SUCCESSFUL!*\n\n"
                f"💰 You stole {format_money(amount)} from @{target.username or 'Unknown'}!\n"
                f"📊 Robberies today: {user.robbery_count_today}/{LIMITS['max_robbery_per_day']}"
            )
        else:
            # Failed
            user.robbery_count_today += 1
            session.commit()
            
            await update.message.reply_text(
                f"🚔 *ROBBERY FAILED!*\n\n"
                f"The police caught you!\n"
                f"📊 Robberies today: {user.robbery_count_today}/{LIMITS['max_robbery_per_day']}"
            )
    finally:
        session.close()

async def kill_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /kill command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to the user you want to kill!")
            return
        
        target_user = update.message.reply_to_message.from_user
        if target_user.id == user.telegram_id:
            await update.message.reply_text("❌ You cannot kill yourself!")
            return
        
        # Check if dead
        if user.is_dead:
            await update.message.reply_text("❌ You cannot kill while dead! Use /medical to revive ($500)")
            return
        
        # Check daily limit
        if is_new_day(user.last_reset_day):
            user.kill_count_today = 0
            user.last_reset_day = datetime.utcnow()
        
        if user.kill_count_today >= LIMITS['max_kills_per_day']:
            await update.message.reply_text(f"❌ You've reached your daily kill limit ({LIMITS['max_kills_per_day']}/day)!")
            return
        
        # Get target
        target = session.query(User).filter_by(telegram_id=target_user.id).first()
        if not target:
            await update.message.reply_text("❌ Target user not found!")
            return
        
        if target.is_dead:
            await update.message.reply_text("❌ Target is already dead!")
            return
        
        # Calculate success chance based on weapon
        weapon_power = WEAPONS.get(user.current_weapon, {}).get('kill_power', 50)
        success_chance = min(weapon_power / 3, 80)  # Max 80% success
        
        if random.random() * 100 < success_chance:
            # Success
            target.is_dead = True
            target.death_time = datetime.utcnow()
            target.health = 0
            user.kill_count_today += 1
            user.balance += 100  # Kill reward
            user.reputation += 5
            
            # Check insurance payout
            insurances = session.query(Insurance).filter_by(
                insured_user_id=target.telegram_id, is_active=True
            ).all()
            for insurance in insurances:
                payout = calculate_insurance_payout(insurance.insurance_type, 1000)
                insurance_owner = session.query(User).filter_by(telegram_id=insurance.owner_id).first()
                if insurance_owner:
                    insurance_owner.balance += payout
            
            session.commit()
            
            await update.message.reply_text(
                f"💀 *KILL SUCCESSFUL!*\n\n"
                f"You killed @{target.username or 'Unknown'}!\n"
                f"💰 Reward: $100\n"
                f"📊 Kills today: {user.kill_count_today}/{LIMITS['max_kills_per_day']}"
            )
        else:
            # Failed
            user.kill_count_today += 1
            user.health -= 1
            session.commit()
            
            await update.message.reply_text(
                f"🛡️ *KILL FAILED!*\n\n"
                f"@{target.username or 'Unknown'} defended themselves!\n"
                f"❤️ You lost 1 health\n"
                f"📊 Kills today: {user.kill_count_today}/{LIMITS['max_kills_per_day']}"
            )
    finally:
        session.close()

async def medical_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /medical command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not user.is_dead and user.health >= user.max_health:
            await update.message.reply_text("❌ You are already at full health!")
            return
        
        cost = 500
        if user.balance < cost:
            await update.message.reply_text(f"❌ You need ${cost:,} for medical treatment!")
            return
        
        user.balance -= cost
        user.is_dead = False
        user.death_time = None
        user.health = user.max_health
        session.commit()
        
        await update.message.reply_text(
            f"🏥 *MEDICAL TREATMENT*\n\n"
            f"✅ You have been revived!\n"
            f"❤️ Health restored to {user.health}/{user.max_health}\n"
            f"💰 Cost: ${cost:,}"
        )
    finally:
        session.close()

async def donateblood_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /donateblood command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to the user you want to donate blood to!")
            return
        
        target_user = update.message.reply_to_message.from_user
        
        # Check if already used today
        if hasattr(user, 'last_blood_donation') and user.last_blood_donation:
            if not is_new_day(user.last_blood_donation):
                await update.message.reply_text("❌ You can only donate blood once per day!")
                return
        
        # Get target
        target = session.query(User).filter_by(telegram_id=target_user.id).first()
        if not target:
            await update.message.reply_text("❌ Target user not found!")
            return
        
        if not target.is_dead and target.health >= target.max_health:
            await update.message.reply_text("❌ Target is already at full health!")
            return
        
        # Revive/heal target
        target.is_dead = False
        target.death_time = None
        target.health = min(target.health + 1, target.max_health)
        user.last_blood_donation = datetime.utcnow()
        user.reputation += 10
        session.commit()
        
        await update.message.reply_text(
            f"🩸 *BLOOD DONATION*\n\n"
            f"✅ You donated blood to @{target.username or 'Unknown'}!\n"
            f"❤️ Their health: {target.health}/{target.max_health}\n"
            f"⭐ Reputation +10"
        )
    finally:
        session.close()

async def insurance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /insurance command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        insurances = session.query(Insurance).filter_by(owner_id=user.telegram_id, is_active=True).all()
        
        text = "🛡️ *YOUR INSURANCE POLICIES*\n═══════════════════\n\n"
        
        if insurances:
            for ins in insurances:
                insured = session.query(User).filter_by(telegram_id=ins.insured_user_id).first()
                if insured:
                    multiplier = ins.payout_multiplier
                    text += f"📋 @{insured.username or 'Unknown'} - ×{multiplier}\n"
        else:
            text += "(No active policies)\n\n"
            text += "Reply to a user with /insurance to insure them!"
        
        text += f"\n📊 Active: {len(insurances)}/{LIMITS['max_insurance']}"
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    finally:
        session.close()
