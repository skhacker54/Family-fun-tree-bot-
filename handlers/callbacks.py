"""
Callback Query Handlers for Fam Tree Bot
=========================================
Handle all inline button interactions
"""

import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from models.database import *
from config.settings import *
from utils.helpers import *
from utils.keyboards import *
from handlers.commands import get_db, get_or_create_user

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main callback handler"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = update.effective_user.id
    
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        # Main menu navigation
        if data == "main_menu":
            await query.edit_message_text(
                "🌳 *MAIN MENU*\n═══════════════════",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_main_menu_keyboard()
            )
        
        # Family menu
        elif data == "menu_family" or data == "family_menu":
            await query.edit_message_text(
                "👨‍👩‍👧 *FAMILY MENU*\n═══════════════════",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_family_menu_keyboard()
            )
        
        elif data == "family_tree":
            await handle_family_tree_callback(query, session, user)
        
        # Account menu
        elif data == "menu_account" or data == "account_menu":
            await query.edit_message_text(
                "💰 *ACCOUNT MENU*\n═══════════════════",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_account_keyboard()
            )
        
        elif data == "account_bank":
            await query.edit_message_text(
                f"🏦 *BANK*\n═══════════════════\n\n"
                f"💰 Wallet: {format_money(user.balance)}\n"
                f"🏦 Bank: {format_money(user.bank_balance)}",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_bank_keyboard()
            )
        
        elif data == "account_weapons":
            await query.edit_message_text(
                "🔫 *WEAPON ARSENAL*\n═══════════════════\n\n"
                f"Current: {user.current_weapon.title()}",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_weapons_keyboard()
            )
        
        elif data == "account_jobs":
            await query.edit_message_text(
                "💼 *JOBS*\n═══════════════════\n\n"
                f"Current: {user.job.title()}",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_jobs_keyboard()
            )
        
        elif data == "account_daily":
            await query.edit_message_text(
                "💰 *DAILY BONUS*\n═══════════════════\n\n"
                "Use /daily to claim your daily reward!",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_account_keyboard()
            )
        
        # Weapon selection
        elif data.startswith("weapon_"):
            weapon = data.replace("weapon_", "")
            if weapon in WEAPONS:
                price = WEAPONS[weapon]['price']
                if user.balance >= price:
                    if user.current_weapon != weapon:
                        user.balance -= price
                    user.current_weapon = weapon
                    session.commit()
                    await query.edit_message_text(
                        f"🔫 *WEAPON EQUIPPED*\n\n"
                        f"You are now using: {weapon.title()}",
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=get_weapons_keyboard()
                    )
                else:
                    await query.answer(f"Need ${price:,} for this weapon!", show_alert=True)
        
        # Job selection
        elif data.startswith("job_"):
            job = data.replace("job_", "")
            if job in JOBS:
                # Check baby sitter requirement
                if job == "baby_sitter":
                    children_count = session.query(FamilyMember).filter_by(parent_id=user.telegram_id).count()
                    if children_count < 3:
                        await query.answer("Baby Sitter requires 3+ children!", show_alert=True)
                        return
                
                user.job = job
                session.commit()
                await query.edit_message_text(
                    f"💼 *JOB CHANGED*\n\n"
                    f"You are now: {job.title()}\n"
                    f"Salary: ${JOBS[job]['salary']:,}/day",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=get_jobs_keyboard()
                )
        
        # Garden menu
        elif data == "menu_garden" or data == "garden_menu":
            plots = session.query(GardenPlot).filter_by(owner_id=user.telegram_id).order_by(GardenPlot.plot_number).all()
            await query.edit_message_text(
                "🌱 *YOUR GARDEN*\n═══════════════════",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_garden_keyboard([{'is_empty': p.is_empty, 'is_ready': p.is_ready, 'crop_type': p.crop_type, 'remaining_time': 0} for p in plots])
            )
        
        elif data == "garden_plant":
            await query.edit_message_text(
                "🌱 *SELECT CROP*\n═══════════════════",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_crop_selection_keyboard()
            )
        
        elif data.startswith("crop_"):
            crop = data.replace("crop_", "")
            if crop in CROPS:
                await query.edit_message_text(
                    f"🌱 *PLANT {crop.upper()}*\n\n"
                    f"Use: /plant {crop} [quantity]\n"
                    f"Or: /plant {crop} * (all empty plots)",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=get_garden_keyboard([])
                )
        
        # Factory menu
        elif data == "menu_factory":
            workers = session.query(Worker).filter_by(owner_id=user.telegram_id).all()
            await query.edit_message_text(
                "🏭 *YOUR FACTORY*\n═══════════════════",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_factory_keyboard([{'id': w.id, 'status': w.status, 'remaining_time': 0} for w in workers])
            )
        
        elif data.startswith("factory_work_"):
            worker_id = int(data.replace("factory_work_", ""))
            worker = session.query(Worker).filter_by(id=worker_id).first()
            if worker and worker.status == 'idle':
                worker.status = 'working'
                worker.work_start_time = datetime.utcnow()
                worker.work_end_time = datetime.utcnow() + timedelta(hours=1)
                session.commit()
                await query.answer("Worker sent to work! (1 hour)", show_alert=True)
        
        elif data.startswith("factory_collect_"):
            worker_id = int(data.replace("factory_collect_", ""))
            worker = session.query(Worker).filter_by(id=worker_id).first()
            if worker and worker.status == 'completed':
                # Give rewards
                user.factory_rating += 1
                user.balance += 3
                
                worker_user = session.query(User).filter_by(telegram_id=worker.worker_id).first()
                if worker_user:
                    worker_user.reputation += 1
                
                worker.status = 'idle'
                worker.work_start_time = None
                worker.work_end_time = None
                session.commit()
                await query.answer("Rewards collected! +1 Rating, +$3", show_alert=True)
        
        # Games menu
        elif data == "menu_games":
            await query.edit_message_text(
                "🎮 *GAMES MENU*\n═══════════════════",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_games_keyboard()
            )
        
        # Market menu
        elif data == "menu_market":
            await query.edit_message_text(
                "🏪 *MARKETPLACE*\n═══════════════════",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_market_keyboard()
            )
        
        # Stats menu
        elif data == "menu_stats":
            await query.edit_message_text(
                "📊 *STATISTICS*\n═══════════════════",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_stats_keyboard()
            )
        
        # Settings menu
        elif data == "menu_settings" or data == "settings_menu":
            await query.edit_message_text(
                "⚙️ *SETTINGS*\n═══════════════════",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_settings_keyboard()
            )
        
        elif data == "settings_language":
            await query.edit_message_text(
                "🌐 *SELECT LANGUAGE*\n═══════════════════",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_language_keyboard()
            )
        
        elif data.startswith("lang_"):
            lang = data.replace("lang_", "")
            if lang in LANGUAGES:
                user.language_code = lang
                session.commit()
                await query.edit_message_text(
                    f"🌐 *LANGUAGE SET*\n\n"
                    f"Language: {LANGUAGES[lang]}",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=get_settings_keyboard()
                )
        
        # Reactions
        elif data.startswith("rxn_"):
            reaction = data.replace("rxn_", "")
            reactions = {
                "hug": "🤗",
                "pat": "🤚",
                "kiss": "😘",
                "sad": "😢",
                "smile": "😊",
                "cry": "😭",
                "slap": "👋",
                "poke": "👉"
            }
            emoji = reactions.get(reaction, "❤️")
            await query.edit_message_text(
                f"{emoji} *{reaction.upper()}*\n\n"
                f"Reply to someone with this reaction!",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_reactions_keyboard()
            )
        
        # Ripple game
        elif data == "ripple_step":
            from handlers.commands3 import active_games
            if user_id in active_games and active_games[user_id]['game'] == 'ripple':
                game = active_games[user_id]
                
                # 2/3 chance for sunflower (win), 1/3 for snake (lose)
                outcome = random.random()
                if outcome < 0.33:
                    # Snake - lose all
                    game['status'] = 'lost'
                    await query.edit_message_text(
                        f"🐍 *SNAKE!*\n\n"
                        f"You lost everything!\n"
                        f"💸 Lost: ${game['bet']:,.0f}",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    del active_games[user_id]
                else:
                    # Sunflower - continue
                    game['multiplier'] *= 1.5
                    if game['multiplier'] >= 20:
                        # Max multiplier reached - auto win
                        winnings = game['bet'] * game['multiplier']
                        user.balance += winnings
                        session.commit()
                        await query.edit_message_text(
                            f"🌻 *MAX MULTIPLIER!*\n\n"
                            f"Multiplier: {game['multiplier']:.1f}×\n"
                            f"💰 Won: ${winnings:,.0f}!",
                            parse_mode=ParseMode.MARKDOWN
                        )
                        del active_games[user_id]
                    else:
                        await query.edit_message_text(
                            f"🌊 *RIPPLE BETTING*\n"
                            f"═══════════════════\n\n"
                            f"💰 Bet: ${game['bet']:,.0f}\n"
                            f"📈 Multiplier: {game['multiplier']:.1f}×\n"
                            f"💵 Potential Win: ${game['bet'] * game['multiplier']:,.0f}\n\n"
                            f"Choose your path:",
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=get_ripple_game_keyboard(game['multiplier'], game['bet'])
                        )
        
        elif data == "ripple_take":
            from handlers.commands3 import active_games
            if user_id in active_games and active_games[user_id]['game'] == 'ripple':
                game = active_games[user_id]
                winnings = game['bet'] * game['multiplier']
                user.balance += winnings
                session.commit()
                await query.edit_message_text(
                    f"💰 *CASHED OUT!*\n\n"
                    f"Multiplier: {game['multiplier']:.1f}×\n"
                    f"💵 Won: ${winnings:,.0f}!",
                    parse_mode=ParseMode.MARKDOWN
                )
                del active_games[user_id]
        
        # Trivia answer
        elif data.startswith("trivia_"):
            answer = data.replace("trivia_", "")
            from handlers.commands3 import active_games
            if user_id in active_games and active_games[user_id]['game'] == 'trivia':
                correct = active_games[user_id]['answer']
                if answer.lower() == correct.lower():
                    user.balance += 50
                    user.reputation += 2
                    session.commit()
                    await query.edit_message_text(
                        f"✅ *CORRECT!*\n\n"
                        f"💰 You won $50!\n"
                        f"⭐ Reputation +2",
                        parse_mode=ParseMode.MARKDOWN
                    )
                else:
                    await query.edit_message_text(
                        f"❌ *WRONG!*\n\n"
                        f"Correct answer: {correct.title()}",
                        parse_mode=ParseMode.MARKDOWN
                    )
                del active_games[user_id]
        
        # Which AI
        elif data in ["whichai_left", "whichai_right"]:
            # 50/50 chance
            correct = random.choice(["whichai_left", "whichai_right"])
            if data == correct:
                user.balance += 25
                session.commit()
                await query.edit_message_text(
                    f"✅ *CORRECT!*\n\n"
                    f"You identified the AI!\n"
                    f"💰 Won $25!",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await query.edit_message_text(
                    f"❌ *WRONG!*\n\n"
                    f"That was the real image!",
                    parse_mode=ParseMode.MARKDOWN
                )
        
        # Adoption confirmation
        elif data.startswith("adopt_yes_"):
            parts = data.split("_")
            parent_id = int(parts[2])
            child_id = int(parts[3])
            
            if user_id == child_id:
                # Create adoption
                adoption = FamilyMember(
                    user_id=child_id,
                    parent_id=parent_id,
                    relationship_type='adopted'
                )
                session.add(adoption)
                session.commit()
                await query.edit_message_text(
                    f"🍼 *ADOPTION COMPLETE!*\n\n"
                    f"Welcome to the family!",
                    parse_mode=ParseMode.MARKDOWN
                )
        
        elif data.startswith("adopt_no_"):
            await query.edit_message_text("❌ Adoption request declined.")
        
        # Marriage confirmation
        elif data.startswith("marry_yes_"):
            parts = data.split("_")
            proposer_id = int(parts[2])
            acceptor_id = int(parts[3])
            
            if user_id == acceptor_id:
                marriage = Partnership(
                    user1_id=proposer_id,
                    user2_id=acceptor_id
                )
                session.add(marriage)
                
                # Give bonuses
                proposer = session.query(User).filter_by(telegram_id=proposer_id).first()
                if proposer:
                    proposer.reputation += 10
                    acceptor = session.query(User).filter_by(telegram_id=acceptor_id).first()
                    if acceptor:
                        acceptor.reputation += 10
                
                session.commit()
                await query.edit_message_text(
                    f"💍 *MARRIAGE COMPLETE!*\n\n"
                    f"Congratulations to the happy couple!\n"
                    f"⭐ Reputation +10 for both!",
                    parse_mode=ParseMode.MARKDOWN
                )
        
        elif data.startswith("marry_no_"):
            await query.edit_message_text("💔 Marriage proposal declined.")
        
        # Hire confirmation
        elif data.startswith("hire_yes_"):
            parts = data.split("_")
            owner_id = int(parts[2])
            worker_id = int(parts[3])
            price = int(parts[4])
            
            if user_id == owner_id:
                owner = session.query(User).filter_by(telegram_id=owner_id).first()
                if owner and owner.balance >= price:
                    owner.balance -= price
                    
                    worker = Worker(
                        owner_id=owner_id,
                        worker_id=worker_id,
                        price=price,
                        rating=0,
                        status='idle'
                    )
                    session.add(worker)
                    session.commit()
                    await query.edit_message_text(
                        f"👷 *WORKER HIRED!*\n\n"
                        f"Cost: ${price:,}",
                        parse_mode=ParseMode.MARKDOWN
                    )
        
        elif data.startswith("hire_no_"):
            await query.edit_message_text("❌ Hiring cancelled.")
        
        # Toggle settings
        elif data.startswith("toggle_"):
            setting = data.replace("toggle_", "")
            settings = user.settings or {}
            current = settings.get(f"{setting}_enabled", True)
            settings[f"{setting}_enabled"] = not current
            user.settings = settings
            session.commit()
            
            status = "enabled" if not current else "disabled"
            await query.answer(f"{setting.title()} {status}!")
            await toggle_command(update, context)
        
        # Scope settings
        elif data.startswith("scope_"):
            scope = data.replace("scope_", "")
            settings = user.settings or {}
            settings['tree_scope'] = scope
            user.settings = settings
            session.commit()
            await query.answer(f"Tree scope set to {scope}!")
            await scope_command(update, context)
        
        # Auto prune settings
        elif data.startswith("prune_"):
            seconds = int(data.replace("prune_", ""))
            settings = user.settings or {}
            settings['auto_prune'] = seconds
            user.settings = settings
            session.commit()
            await query.answer(f"Auto-prune set to {format_time(seconds)}!")
            await autoprune_command(update, context)
        
        # Admin panel
        elif data == "admin_panel":
            await query.edit_message_text(
                "🔧 *ADMIN PANEL*\n═══════════════════",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_admin_keyboard()
            )
        
        # Help
        elif data == "menu_help":
            await query.edit_message_text(
                "❓ *HELP*\n═══════════════════\n\n"
                "Use /help for full command list!\n\n"
                "Quick links:\n"
                "• /start - Main menu\n"
                "• /account - Your profile\n"
                "• /tree - Family tree\n"
                "• /daily - Daily bonus\n"
                "• /help - All commands",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_main_menu_keyboard()
            )
        
        else:
            await query.answer("Feature coming soon!")
    
    finally:
        session.close()

async def handle_family_tree_callback(query, session, user):
    """Handle family tree display"""
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
    
    await query.edit_message_text(
        tree_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_family_menu_keyboard()
    )
