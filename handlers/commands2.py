"""
Additional Command Handlers (Part 2)
=====================================
Daily, Factory, Garden, Trading, Cooking, Games commands
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

# ==================== MODULE 4: DAILY REWARDS ====================

async def daily_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /daily command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        # Check if already claimed today
        if user.last_daily:
            time_since = datetime.utcnow() - user.last_daily
            if time_since < timedelta(hours=24):
                remaining = timedelta(hours=24) - time_since
                hours, remainder = divmod(int(remaining.total_seconds()), 3600)
                minutes, _ = divmod(remainder, 60)
                await update.message.reply_text(
                    f"⏰ *Daily Bonus Already Claimed!*\n\n"
                    f"Come back in {hours}h {minutes}m"
                )
                return
        
        # Calculate reward
        family_count = session.query(FamilyMember).filter_by(parent_id=user.telegram_id).count()
        job_salary = JOBS.get(user.job, {}).get('salary', 0)
        reward = calculate_daily_reward(family_count, job_salary)
        
        # Apply streak bonus
        streak_bonus = 0
        if user.last_daily and (datetime.utcnow() - user.last_daily) < timedelta(hours=48):
            user.daily_streak += 1
            streak_bonus = min(user.daily_streak * 10, 100)  # Max 100 bonus
        else:
            user.daily_streak = 1
        
        total_reward = reward + streak_bonus
        user.balance += total_reward
        user.last_daily = datetime.utcnow()
        
        # Assign new gemstone
        user.gemstone = get_random_gemstone()
        
        session.commit()
        
        await update.message.reply_text(
            f"✨ *DAILY BONUS CLAIMED!*\n\n"
            f"💰 Base Reward: ${reward:,}\n"
            f"🔥 Streak: {user.daily_streak} days (+${streak_bonus:,})\n"
            f"💎 Gemstone: {user.gemstone.title()}\n"
            f"═══════════════════\n"
            f"💵 Total: ${total_reward:,}\n\n"
            f"💰 New Balance: {format_money(user.balance)}"
        )
    finally:
        session.close()

async def fuse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /fuse command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to a user with the same gemstone to fuse!")
            return
        
        target_user = update.message.reply_to_message.from_user
        target = session.query(User).filter_by(telegram_id=target_user.id).first()
        
        if not target:
            await update.message.reply_text("❌ Target user not found!")
            return
        
        if not user.gemstone or not target.gemstone:
            await update.message.reply_text("❌ Both users need a gemstone!")
            return
        
        if user.gemstone != target.gemstone:
            await update.message.reply_text(
                f"❌ Gemstones don't match!\n"
                f"Your gemstone: {user.gemstone.title()}\n"
                f"Their gemstone: {target.gemstone.title()}"
            )
            return
        
        # Fuse gemstones
        reward = GEMSTONE_FUSE_REWARD
        user.balance += reward
        target.balance += reward
        user.gemstone = get_random_gemstone()  # New random gemstone
        target.gemstone = get_random_gemstone()
        
        session.commit()
        
        await update.message.reply_text(
            f"💎 *GEMSTONE FUSION!*\n\n"
            f"✅ {user.gemstone.title()} + {target.gemstone.title()} fused!\n"
            f"💰 Both received ${reward:,}!\n\n"
            f"🎲 New gemstones assigned!"
        )
    finally:
        session.close()

async def reactions_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /reactions command"""
    await update.message.reply_text(
        "😊 *REACTIONS MENU*\n"
        "═══════════════════\n\n"
        "Select a reaction:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_reactions_keyboard()
    )

# ==================== MODULE 5: FACTORY COMMANDS ====================

async def factory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /factory command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        workers = session.query(Worker).filter_by(owner_id=user.telegram_id).all()
        
        text = f"""
🏭 *YOUR FACTORY*
═══════════════════

⭐ Rating: {user.factory_rating}
👷 Workers: {len(workers)}/{LIMITS['max_workers']}

"""
        if workers:
            for i, worker in enumerate(workers, 1):
                worker_user = session.query(User).filter_by(telegram_id=worker.worker_id).first()
                username = worker_user.username if worker_user else 'Unknown'
                
                if worker.status == 'working' and worker.work_end_time:
                    remaining = calculate_time_remaining(worker.work_end_time)
                    if remaining == 0:
                        worker.status = 'completed'
                        session.commit()
                        status = "Completed ✓"
                    else:
                        status = f"Working ({format_time(remaining)} left)"
                elif worker.status == 'completed':
                    status = "Completed ✓ [Collect]"
                else:
                    status = "Idle"
                
                text += f"{i}. @{username} - {status}\n"
        else:
            text += "(No workers hired)\n\nReply to a user with /hire to hire them!"
        
        await update.message.reply_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_factory_keyboard([{'id': w.id, 'status': w.status, 'remaining_time': calculate_time_remaining(w.work_end_time) if w.work_end_time else 0} for w in workers])
        )
    finally:
        session.close()

async def hire_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /hire command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to the user you want to hire!")
            return
        
        target_user = update.message.reply_to_message.from_user
        
        if target_user.id == user.telegram_id:
            await update.message.reply_text("❌ You cannot hire yourself!")
            return
        
        # Check workers limit
        workers_count = session.query(Worker).filter_by(owner_id=user.telegram_id).count()
        if workers_count >= LIMITS['max_workers']:
            await update.message.reply_text(f"❌ You already have {LIMITS['max_workers']} workers (max limit)!")
            return
        
        # Check if already hired
        existing = session.query(Worker).filter_by(
            owner_id=user.telegram_id, worker_id=target_user.id
        ).first()
        if existing:
            await update.message.reply_text("❌ You already hired this user!")
            return
        
        # Get or create target user
        target = session.query(User).filter_by(telegram_id=target_user.id).first()
        if not target:
            target = get_or_create_user(target_user, session)
        
        # Check if target is already employed
        employed = session.query(Worker).filter_by(worker_id=target_user.id).first()
        if employed:
            await update.message.reply_text("❌ This user is already employed by someone else!")
            return
        
        # Calculate price
        price = calculate_worker_price(target.reputation, target.balance)
        
        if user.balance < price:
            await update.message.reply_text(f"❌ You need {format_money(price)} to hire this worker!")
            return
        
        # Confirm hire
        await update.message.reply_text(
            f"👷 *HIRE WORKER*\n\n"
            f"User: @{target.username or 'Unknown'}\n"
            f"Price: {format_money(price)}\n"
            f"Rating: {target.reputation}\n\n"
            f"Do you want to hire?",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_confirmation_keyboard(
                f"hire_yes_{user.telegram_id}_{target_user.id}_{int(price)}",
                f"hire_no_{user.telegram_id}_{target_user.id}"
            )
        )
    finally:
        session.close()

async def fire_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /fire command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to the worker you want to fire!")
            return
        
        target_user = update.message.reply_to_message.from_user
        
        worker = session.query(Worker).filter_by(
            owner_id=user.telegram_id, worker_id=target_user.id
        ).first()
        
        if not worker:
            await update.message.reply_text("❌ This user is not your worker!")
            return
        
        # Calculate sell price (current price)
        target = session.query(User).filter_by(telegram_id=target_user.id).first()
        sell_price = calculate_worker_price(target.reputation if target else 0, target.balance if target else 0)
        
        user.balance += sell_price
        session.delete(worker)
        session.commit()
        
        await update.message.reply_text(
            f"🚪 *WORKER FIRED*\n\n"
            f"@{target.username if target else 'Unknown'} has been fired.\n"
            f"💰 You received {format_money(sell_price)}"
        )
    finally:
        session.close()

# ==================== MODULE 6: GARDEN COMMANDS ====================

async def garden_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /garden command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        plots = session.query(GardenPlot).filter_by(owner_id=user.telegram_id).order_by(GardenPlot.plot_number).all()
        
        # Ensure all plots exist
        if len(plots) < user.garden_slots:
            for i in range(len(plots) + 1, user.garden_slots + 1):
                plot = GardenPlot(owner_id=user.telegram_id, plot_number=i, is_empty=True)
                session.add(plot)
            session.commit()
            plots = session.query(GardenPlot).filter_by(owner_id=user.telegram_id).order_by(GardenPlot.plot_number).all()
        
        text = f"""
🌱 *YOUR GARDEN*
═══════════════════
Season: {get_current_season().title()}
Slots: {len([p for p in plots if not p.is_empty])}/{user.garden_slots}

"""
        
        # Display garden grid
        for i in range(0, len(plots), 3):
            row_text = ""
            for j in range(3):
                idx = i + j
                if idx < len(plots):
                    plot = plots[idx]
                    if plot.is_empty:
                        row_text += "[🟫] "
                    elif plot.is_ready:
                        crop_emoji = {"pepper": "🌶️", "potato": "🥔", "eggplant": "🍆", 
                                     "carrot": "🥕", "corn": "🌽", "tomato": "🍅"}.get(plot.crop_type, "🌱")
                        row_text += f"[{crop_emoji}] "
                    else:
                        remaining = calculate_time_remaining(plot.planted_at + timedelta(seconds=plot.growth_time)) if plot.planted_at else 0
                        row_text += f"[🌱{remaining//60}m] "
            text += row_text + "\n"
        
        text += "\n🟫 = Empty | 🌱 = Growing | 🌶️ = Ready"
        
        await update.message.reply_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_garden_keyboard([{'is_empty': p.is_empty, 'is_ready': p.is_ready, 'crop_type': p.crop_type, 'remaining_time': calculate_time_remaining(p.planted_at + timedelta(seconds=p.growth_time)) if p.planted_at and p.growth_time else 0} for p in plots])
        )
    finally:
        session.close()

async def plant_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /plant command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not context.args:
            await update.message.reply_text(
                "❌ Usage: /plant [crop] [quantity]\n"
                "Examples:\n"
                "/plant corn 5\n"
                "/plant tomato * (plant all empty)"
            )
            return
        
        crop_name = context.args[0].lower()
        
        if crop_name not in CROPS:
            await update.message.reply_text(
                f"❌ Invalid crop! Available: {', '.join(CROPS.keys())}"
            )
            return
        
        # Get empty plots
        empty_plots = session.query(GardenPlot).filter_by(
            owner_id=user.telegram_id, is_empty=True
        ).all()
        
        if not empty_plots:
            await update.message.reply_text("❌ No empty plots available!")
            return
        
        # Determine quantity
        if len(context.args) > 1 and context.args[1] == '*':
            quantity = len(empty_plots)
        elif len(context.args) > 1:
            try:
                quantity = min(int(context.args[1]), len(empty_plots))
            except:
                quantity = 1
        else:
            quantity = 1
        
        crop_info = CROPS[crop_name]
        total_cost = crop_info['buy_price'] * quantity
        
        if user.balance < total_cost:
            await update.message.reply_text(f"❌ You need {format_money(total_cost)} to plant!")
            return
        
        # Plant crops
        season = get_current_season()
        growth_time = crop_info['growth_time']
        
        # Apply season bonus
        if crop_info['season'] == season or crop_info['season'] == 'all':
            growth_time = growth_time // 2  # 2x speed during right season
        
        for i in range(quantity):
            plot = empty_plots[i]
            plot.crop_type = crop_name
            plot.planted_at = datetime.utcnow()
            plot.growth_time = growth_time
            plot.is_empty = False
            plot.is_ready = False
        
        user.balance -= total_cost
        session.commit()
        
        await update.message.reply_text(
            f"🌱 *PLANTED!*\n\n"
            f"Crop: {crop_name.title()}\n"
            f"Quantity: {quantity}\n"
            f"Cost: {format_money(total_cost)}\n"
            f"Growth time: {format_time(growth_time)}\n"
            f"{'⚡ Season bonus applied!' if crop_info['season'] == season or crop_info['season'] == 'all' else ''}"
        )
    finally:
        session.close()

async def harvest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /harvest command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        # Get ready plots
        plots = session.query(GardenPlot).filter_by(owner_id=user.telegram_id, is_ready=True).all()
        
        if not plots:
            # Check for plots that should be ready
            all_plots = session.query(GardenPlot).filter_by(owner_id=user.telegram_id, is_empty=False).all()
            now = datetime.utcnow()
            ready_plots = []
            for plot in all_plots:
                if plot.planted_at and plot.growth_time:
                    ready_time = plot.planted_at + timedelta(seconds=plot.growth_time)
                    if now >= ready_time:
                        plot.is_ready = True
                        ready_plots.append(plot)
            
            if ready_plots:
                plots = ready_plots
                session.commit()
            else:
                await update.message.reply_text("❌ No crops ready to harvest!")
                return
        
        # Harvest crops
        harvested = {}
        for plot in plots:
            crop = plot.crop_type
            if crop not in harvested:
                harvested[crop] = 0
            harvested[crop] += 1
            
            # Reset plot
            plot.is_empty = True
            plot.is_ready = False
            plot.crop_type = None
            plot.planted_at = None
            plot.growth_time = 0
        
        # Add to barn
        for crop, quantity in harvested.items():
            barn_item = session.query(BarnItem).filter_by(
                owner_id=user.telegram_id, item_name=crop
            ).first()
            if barn_item:
                barn_item.quantity += quantity
            else:
                barn_item = BarnItem(
                    owner_id=user.telegram_id,
                    item_type='crop',
                    item_name=crop,
                    quantity=quantity
                )
                session.add(barn_item)
        
        session.commit()
        
        harvest_text = "🌾 *HARVEST COMPLETE!*\n\n"
        for crop, quantity in harvested.items():
            harvest_text += f"{crop.title()}: {quantity}\n"
        
        await update.message.reply_text(harvest_text, parse_mode=ParseMode.MARKDOWN)
    finally:
        session.close()

async def barn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /barn command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        items = session.query(BarnItem).filter_by(owner_id=user.telegram_id).all()
        
        text = "🏚️ *YOUR BARN*\n═══════════════════\n\n"
        
        if items:
            total_items = sum(item.quantity for item in items)
            for item in items:
                emoji = {"pepper": "🌶️", "potato": "🥔", "eggplant": "🍆", 
                        "carrot": "🥕", "corn": "🌽", "tomato": "🍅"}.get(item.item_name, "📦")
                text += f"{emoji} {item.item_name.title()}: {item.quantity}\n"
            text += f"\n📊 Total: {total_items}/{user.barn_size}"
        else:
            text += "(Barn is empty)\n\nPlant crops in your garden!"
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    finally:
        session.close()

async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /add command (buy seeds)"""
    await update.message.reply_text(
        "🛒 *BUY SEEDS*\n"
        "═══════════════════\n\n"
        "Select crop to buy:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_crop_selection_keyboard()
    )

async def sell_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /sell command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not context.args:
            await update.message.reply_text(
                "❌ Usage: /sell [crop] [quantity]\n"
                "Example: /sell corn 10"
            )
            return
        
        crop_name = context.args[0].lower()
        
        if len(context.args) > 1:
            try:
                quantity = int(context.args[1])
            except:
                quantity = 1
        else:
            quantity = 1
        
        barn_item = session.query(BarnItem).filter_by(
            owner_id=user.telegram_id, item_name=crop_name
        ).first()
        
        if not barn_item or barn_item.quantity < quantity:
            await update.message.reply_text("❌ Not enough crops in barn!")
            return
        
        if crop_name not in CROPS:
            await update.message.reply_text("❌ Invalid crop!")
            return
        
        sell_price = CROPS[crop_name]['sell_price'] * quantity
        
        barn_item.quantity -= quantity
        if barn_item.quantity == 0:
            session.delete(barn_item)
        
        user.balance += sell_price
        session.commit()
        
        await update.message.reply_text(
            f"💰 *SOLD!*\n\n"
            f"Crop: {crop_name.title()}\n"
            f"Quantity: {quantity}\n"
            f"Earned: {format_money(sell_price)}"
        )
    finally:
        session.close()

async def boost_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /boost command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not context.args:
            await update.message.reply_text(
                "❌ Usage: /boost [plot_number]\n"
                "Example: /boost 1"
            )
            return
        
        try:
            plot_number = int(context.args[0])
        except:
            await update.message.reply_text("❌ Invalid plot number!")
            return
        
        plot = session.query(GardenPlot).filter_by(
            owner_id=user.telegram_id, plot_number=plot_number
        ).first()
        
        if not plot or plot.is_empty:
            await update.message.reply_text("❌ Plot is empty!")
            return
        
        if plot.is_ready:
            await update.message.reply_text("❌ Crop is already ready!")
            return
        
        cost = 30
        if user.balance < cost:
            await update.message.reply_text(f"❌ You need ${cost} for boost!")
            return
        
        # Reduce growth time
        plot.growth_time = max(plot.growth_time - 3600, 0)  # -1 hour or instant
        user.balance -= cost
        session.commit()
        
        remaining = calculate_time_remaining(plot.planted_at + timedelta(seconds=plot.growth_time)) if plot.planted_at else 0
        
        await update.message.reply_text(
            f"⚡ *BOOSTED!*\n\n"
            f"Plot {plot_number} boosted!\n"
            f"Time saved: 1 hour\n"
            f"Remaining: {format_time(remaining)}\n"
            f"Cost: ${cost}"
        )
    finally:
        session.close()

async def refill_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /refill command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        cost = 1000
        if user.balance < cost:
            await update.message.reply_text(f"❌ You need ${cost:,} to refill orders!")
            return
        
        user.balance -= cost
        session.commit()
        
        await update.message.reply_text(
            f"🔄 *ORDERS REFILLED!*\n\n"
            f"New orders are available!\n"
            f"Cost: ${cost:,}"
        )
    finally:
        session.close()

# ==================== MODULE 7: TRADING COMMANDS ====================

async def stands_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stands command"""
    session = get_db()
    try:
        # Get all active listings grouped by crop
        listings = session.query(MarketListing).filter_by(is_active=True).all()
        
        crop_counts = {}
        for listing in listings:
            if listing.crop_type not in crop_counts:
                crop_counts[listing.crop_type] = 0
            crop_counts[listing.crop_type] += 1
        
        text = "🏪 *GLOBAL MARKETPLACE*\n═══════════════════\n\n"
        text += "Select crop to buy:\n\n"
        
        for crop, count in sorted(crop_counts.items()):
            emoji = {"pepper": "🌶️", "potato": "🥔", "eggplant": "🍆", 
                    "carrot": "🥕", "corn": "🌽", "tomato": "🍅"}.get(crop, "🌱")
            text += f"{emoji} {crop.title()} ({count} listings)\n"
        
        if not crop_counts:
            text += "(No active listings)\n\nUse /putstand to sell items!"
        
        await update.message.reply_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_market_keyboard()
        )
    finally:
        session.close()

async def putstand_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /putstand command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        # Parse command: /putstand corn 50 150 or /putstand 50 corn for 3 each
        if len(context.args) < 3:
            await update.message.reply_text(
                "❌ Usage:\n"
                "/putstand [crop] [quantity] [price]\n"
                "/putstand [quantity] [crop] for [price] each\n\n"
                "Examples:\n"
                "/putstand corn 50 150\n"
                "/putstand 50 corn for 3 each"
            )
            return
        
        # Simple parsing (first format)
        crop_name = context.args[0].lower()
        try:
            quantity = int(context.args[1])
            price = float(context.args[2])
        except:
            await update.message.reply_text("❌ Invalid quantity or price!")
            return
        
        if crop_name not in CROPS:
            await update.message.reply_text(f"❌ Invalid crop! Available: {', '.join(CROPS.keys())}")
            return
        
        # Check max price (3x selling price)
        max_price = CROPS[crop_name]['sell_price'] * 3
        if price > max_price:
            await update.message.reply_text(f"❌ Max price is ${max_price} per unit!")
            return
        
        # Check barn
        barn_item = session.query(BarnItem).filter_by(
            owner_id=user.telegram_id, item_name=crop_name
        ).first()
        
        if not barn_item or barn_item.quantity < quantity:
            await update.message.reply_text("❌ Not enough crops in barn!")
            return
        
        # Remove from barn
        barn_item.quantity -= quantity
        if barn_item.quantity == 0:
            session.delete(barn_item)
        
        # Create listing
        listing = MarketListing(
            seller_id=user.telegram_id,
            crop_type=crop_name,
            quantity=quantity,
            price_per_unit=price
        )
        session.add(listing)
        session.commit()
        
        await update.message.reply_text(
            f"🏪 *LISTING CREATED!*\n\n"
            f"Crop: {crop_name.title()}\n"
            f"Quantity: {quantity}\n"
            f"Price: ${price}/unit\n"
            f"Total value: ${price * quantity:.0f}"
        )
    finally:
        session.close()

async def stand_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stand command"""
    session = get_db()
    try:
        # Get target user (mentioned or self)
        if update.message.reply_to_message:
            target_user = update.message.reply_to_message.from_user
        elif context.args:
            username = context.args[0].replace('@', '')
            target = session.query(User).filter_by(username=username).first()
            if not target:
                await update.message.reply_text("❌ User not found!")
                return
            target_user = type('obj', (object,), {'id': target.telegram_id, 'username': target.username})()
        else:
            target_user = update.effective_user
        
        listings = session.query(MarketListing).filter_by(
            seller_id=target_user.id, is_active=True
        ).all()
        
        text = f"🏪 *@{target_user.username or 'Unknown'}'s STAND*\n═══════════════════\n\n"
        
        if listings:
            total_value = 0
            for i, listing in enumerate(listings, 1):
                value = listing.quantity * listing.price_per_unit
                total_value += value
                text += f"{i}. {listing.crop_type.title()} ×{listing.quantity} - ${value:.0f}\n"
            text += f"\n💰 Total Value: ${total_value:.0f}"
        else:
            text += "(No active listings)"
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    finally:
        session.close()

async def gift_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /gift command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to the user you want to gift!")
            return
        
        if len(context.args) < 2:
            await update.message.reply_text("❌ Usage: /gift [crop] [quantity]")
            return
        
        crop_name = context.args[0].lower()
        try:
            quantity = int(context.args[1])
        except:
            await update.message.reply_text("❌ Invalid quantity!")
            return
        
        target_user = update.message.reply_to_message.from_user
        
        # Check barn
        barn_item = session.query(BarnItem).filter_by(
            owner_id=user.telegram_id, item_name=crop_name
        ).first()
        
        if not barn_item or barn_item.quantity < quantity:
            await update.message.reply_text("❌ Not enough crops in barn!")
            return
        
        # Remove from sender's barn
        barn_item.quantity -= quantity
        if barn_item.quantity == 0:
            session.delete(barn_item)
        
        # Add to recipient's barn
        target_barn = session.query(BarnItem).filter_by(
            owner_id=target_user.id, item_name=crop_name
        ).first()
        if target_barn:
            target_barn.quantity += quantity
        else:
            target_barn = BarnItem(
                owner_id=target_user.id,
                item_type='crop',
                item_name=crop_name,
                quantity=quantity
            )
            session.add(target_barn)
        
        session.commit()
        
        await update.message.reply_text(
            f"🎁 *GIFT SENT!*\n\n"
            f"📦 {quantity} {crop_name.title()}\n"
            f"👤 To: @{target_user.username or 'Unknown'}"
        )
    finally:
        session.close()

# ==================== MODULE 8: COOKING COMMANDS ====================

async def cook_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cook command"""
    session = get_db()
    try:
        user = get_or_create_user(update.effective_user, session)
        
        if context.args:
            # Quick cook
            recipe_name = context.args[0].lower()
            if recipe_name not in RECIPES:
                await update.message.reply_text(f"❌ Invalid recipe! Available: {', '.join(RECIPES.keys())}")
                return
            
            quantity = int(context.args[1]) if len(context.args) > 1 else 1
            recipe = RECIPES[recipe_name]
            
            # Check ingredients
            for ingredient, amount in recipe['ingredients'].items():
                barn_item = session.query(BarnItem).filter_by(
                    owner_id=user.telegram_id, item_name=ingredient
                ).first()
                if not barn_item or barn_item.quantity < amount * quantity:
                    await update.message.reply_text(f"❌ Not enough {ingredient}!")
                    return
            
            # Remove ingredients
            for ingredient, amount in recipe['ingredients'].items():
                barn_item = session.query(BarnItem).filter_by(
                    owner_id=user.telegram_id, item_name=ingredient
                ).first()
                barn_item.quantity -= amount * quantity
                if barn_item.quantity == 0:
                    session.delete(barn_item)
            
            # Add product
            product_name = recipe_name
            product = session.query(BarnItem).filter_by(
                owner_id=user.telegram_id, item_name=product_name
            ).first()
            if product:
                product.quantity += quantity
            else:
                product = BarnItem(
                    owner_id=user.telegram_id,
                    item_type='recipe',
                    item_name=product_name,
                    quantity=quantity
                )
                session.add(product)
            
            session.commit()
            
            await update.message.reply_text(
                f"🍳 *COOKING COMPLETE!*\n\n"
                f"Recipe: {recipe_name.title()}\n"
                f"Quantity: {quantity}\n"
                f"Time: {format_time(recipe['time'])}"
            )
            return
        
        # Show cooking menu
        text = "🍳 *COOKING BENCH*\n═══════════════════\n\n"
        text += "*Available Recipes:*\n\n"
        
        for recipe_name, recipe in RECIPES.items():
            text += f"*{recipe_name.title()}*\n"
            text += "Ingredients:\n"
            for ingredient, amount in recipe['ingredients'].items():
                text += f"  - {ingredient}: {amount}\n"
            text += f"Time: {format_time(recipe['time'])}\n\n"
        
        text += "Use `/cook [recipe] [quantity]` to cook!"
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    finally:
        session.close()

async def stove_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stove command"""
    await cook_command(update, context)
