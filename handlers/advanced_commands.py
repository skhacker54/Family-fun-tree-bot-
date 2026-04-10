"""
Advanced Commands for Fam Tree Bot
===================================
AI, Blockchain, Clan, Quest, and other advanced features
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from models.database import get_session, init_db_engine, User
from services.ai_service import ai_service
from services.blockchain_service import blockchain_service
from services.visual_service import visual_service
from games.rpg_battle import RPGCharacter, BattleSystem, start_battle, get_battle, end_battle
from games.casino import SlotMachine, Blackjack, DiceGame, create_game, get_game, end_game
from games.dungeon import create_dungeon, get_dungeon, end_dungeon
from games.quests import get_quest_system
from achievements.manager import get_achievement_manager
from clans.manager import clan_manager
from api.external import api_service

# ==================== AI COMMANDS ====================

async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ai command - AI Family Assistant"""
    user_id = update.effective_user.id
    
    advice = ai_service.get_family_advice({"user_id": user_id})
    
    await update.message.reply_text(
        f"🤖 *AI FAMILY ASSISTANT*\n═══════════════════\n\n{advice}",
        parse_mode=ParseMode.MARKDOWN
    )

async def aigen_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /aigen command - AI Image Generation"""
    if not context.args:
        await update.message.reply_text(
            "❌ Usage: /aigen [description]\n"
            "Example: /aigen a beautiful family portrait"
        )
        return
    
    prompt = ' '.join(context.args)
    
    await update.message.reply_text(
        f"🎨 *AI IMAGE GENERATION*\n═══════════════════\n\n"
        f"Prompt: {prompt}\n\n"
        f"🖼️ Generating image...\n"
        f"_(Connect to DALL-E or Stable Diffusion for real generation)_",
        parse_mode=ParseMode.MARKDOWN
    )

async def smart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /smart command - Smart recommendations"""
    user_id = update.effective_user.id
    
    recommendation = ai_service.get_garden_recommendation("spring", [])
    
    await update.message.reply_text(
        f"💡 *SMART RECOMMENDATIONS*\n═══════════════════\n\n{recommendation}",
        parse_mode=ParseMode.MARKDOWN
    )

# ==================== BLOCKCHAIN COMMANDS ====================

async def nft_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /nft command - NFT collection"""
    user_id = update.effective_user.id
    
    nfts = blockchain_service.get_user_nfts(user_id)
    
    text = "╔══════════════════════════════════════════════════════════════╗\n"
    text += "║                    🎨 YOUR NFT COLLECTION                    ║\n╠══════════════════════════════════════════════════════════════╣\n"
    
    if nfts:
        total_value = 0
        for nft in nfts:
            value = blockchain_service.calculate_nft_value(nft)
            total_value += value
            rarity_emoji = {"common": "⚪", "rare": "🔵", "epic": "🟣", "legendary": "🟡"}.get(nft.get("rarity"), "⚪")
            text += f"║  {rarity_emoji} {nft['name'][:25]:<25} ${value:,}          ║\n"
        text += f"║                                                              ║\n"
        text += f"║  💰 Total Value: ${total_value:,}                            ║\n"
    else:
        text += "║  (No NFTs yet)                                               ║\n"
        text += "║  Complete achievements to earn NFT badges!                   ║\n"
    
    text += "╚══════════════════════════════════════════════════════════════╝"
    
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def crypto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /crypto command - Crypto wallet"""
    await update.message.reply_text(
        "💎 *CRYPTO WALLET*\n═══════════════════\n\n"
        "BTC: 0.00000000\n"
        "ETH: 0.00000000\n"
        "SOL: 0.00000000\n\n"
        "_(Connect wallet to enable crypto features)_",
        parse_mode=ParseMode.MARKDOWN
    )

async def mint_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /mint command - Mint NFT"""
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text(
            "❌ Usage: /mint [badge_type]\n"
            f"Available: {', '.join(blockchain_service.NFT_BADGES.keys())}"
        )
        return
    
    badge_type = context.args[0].lower()
    nft = blockchain_service.mint_badge(user_id, badge_type)
    
    if nft:
        await update.message.reply_text(
            f"🎉 *NFT MINTED!*\n═══════════════════\n\n"
            f"Name: {nft['name']}\n"
            f"Rarity: {nft['rarity'].upper()}\n"
            f"Token ID: `{nft['token_id']}`\n"
            f"Blockchain: {nft['blockchain']}\n\n"
            f"View on OpenSea: [Link](https://opensea.io/assets/{nft['token_id']})",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text("❌ Invalid badge type!")

# ==================== CLAN COMMANDS ====================

async def clan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clan command - Clan management"""
    user_id = update.effective_user.id
    
    clan_id = clan_manager.user_clan.get(user_id)
    
    if clan_id:
        visual = clan_manager.get_clan_visual(clan_id)
        await update.message.reply_text(visual, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(
            "⚔️ *CLAN SYSTEM*\n═══════════════════\n\n"
            "You are not in a clan!\n\n"
            "Commands:\n"
            "/clancreate [name] [tag] - Create clan\n"
            "/clanjoin [clan_id] - Join clan\n"
            "/clanlist - List clans",
            parse_mode=ParseMode.MARKDOWN
        )

async def clancreate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clancreate command"""
    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"
    
    if len(context.args) < 2:
        await update.message.reply_text("❌ Usage: /clancreate [name] [tag]")
        return
    
    name = context.args[0]
    tag = context.args[1]
    description = ' '.join(context.args[2:]) if len(context.args) > 2 else "No description"
    
    clan = clan_manager.create_clan(name, tag, description, user_id, username)
    
    if clan:
        await update.message.reply_text(
            f"⚔️ *CLAN CREATED!*\n═══════════════════\n\n"
            f"Name: {clan.name}\n"
            f"Tag: [{clan.tag}]\n"
            f"ID: `{clan.id}`\n\n"
            f"Use /claninvite @[username] to invite members!",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text("❌ Could not create clan. You may already be in one or tag is taken.")

async def clanlist_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clanlist command"""
    clans = clan_manager.get_leaderboard()
    
    text = "╔══════════════════════════════════════════════════════════════╗\n"
    text += "║                    🏆 TOP CLANS                              ║\n╠══════════════════════════════════════════════════════════════╣\n"
    
    for i, clan in enumerate(clans[:10], 1):
        text += f"║  {i}. [{clan.tag}] {clan.name[:20]:<20} Lv.{clan.level}          ║\n"
    
    text += "╚══════════════════════════════════════════════════════════════╝"
    
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

# ==================== QUEST COMMANDS ====================

async def quest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /quest command - View quests"""
    user_id = update.effective_user.id
    
    quest_system = get_quest_system(user_id)
    visual = quest_system.get_quest_visual()
    
    await update.message.reply_text(visual, parse_mode=ParseMode.MARKDOWN)

# ==================== ACHIEVEMENT COMMANDS ====================

async def achievements_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /achievements command"""
    user_id = update.effective_user.id
    
    achievement_manager = get_achievement_manager(user_id)
    visual = achievement_manager.get_achievement_visual()
    
    await update.message.reply_text(visual, parse_mode=ParseMode.MARKDOWN)

# ==================== RPG BATTLE COMMANDS ====================

async def battle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /battle command - Start RPG battle"""
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to the user you want to battle!")
        return
    
    user1 = update.effective_user
    user2 = update.message.reply_to_message.from_user
    
    battle_id = start_battle(user1.id, user1.username or "Player1", 
                             user2.id, user2.username or "Player2")
    battle = get_battle(battle_id)
    
    await update.message.reply_text(
        battle.get_battle_visual() + "\n\n"
        "Use /battleattack to attack or /battleskill [skill] for special moves!",
        parse_mode=ParseMode.MARKDOWN
    )

async def battleattack_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /battleattack command"""
    user_id = update.effective_user.id
    
    # Find user's active battle
    battle_id = None
    for bid, battle in active_battles.items():
        if battle.player1.user_id == user_id or battle.player2.user_id == user_id:
            battle_id = bid
            break
    
    if not battle_id:
        await update.message.reply_text("❌ You are not in a battle!")
        return
    
    battle = get_battle(battle_id)
    result = battle.execute_turn("attack")
    
    text = battle.get_battle_visual() + "\n\n"
    text += "⚔️ *COMBAT LOG*\n"
    for log in result["actions"][0].get("combat_log", []):
        text += f"• {log}\n"
    
    if result.get("finished"):
        text += f"\n🏆 Winner: {result.get('winner')}"
        end_battle(battle_id)
    
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

# ==================== CASINO COMMANDS ====================

async def slots_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /slots command - Slot machine"""
    result, multiplier, win = SlotMachine.spin()
    
    visual = SlotMachine.get_visual(result)
    
    if win:
        if multiplier >= 50:
            visual += "\n🎉 *JACKPOT!* 50× multiplier!"
        elif multiplier >= 10:
            visual += f"\n💎 *BIG WIN!* {multiplier}× multiplier!"
        else:
            visual += f"\n✅ *WIN!* {multiplier}× multiplier!"
    else:
        visual += "\n❌ *No match. Try again!*"
    
    await update.message.reply_text(visual, parse_mode=ParseMode.MARKDOWN)

async def blackjack_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /blackjack command"""
    user_id = update.effective_user.id
    
    game_id = create_game("blackjack", user_id)
    game_data = get_game(game_id)
    
    await update.message.reply_text(
        game_data["game"].get_visual() + "\n\n"
        "Commands:\n"
        "/bjhit - Draw a card\n"
        "/bjstand - Stand\n",
        parse_mode=ParseMode.MARKDOWN
    )

async def bjhit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /bjhit command"""
    user_id = update.effective_user.id
    
    # Find user's game
    for game_id, game_data in casino_games.items():
        if game_data["type"] == "blackjack":
            game = game_data["game"]
            game.hit()
            
            text = game.get_visual()
            
            if game.game_over:
                result = game.get_result()
                text += f"\n\n{result['result'].upper()}: {result['reason']}"
                end_game(game_id)
            else:
                text += "\n\n/bjhit or /bjstand?"
            
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
            return
    
    await update.message.reply_text("❌ No active blackjack game! Start with /blackjack")

# ==================== DUNGEON COMMANDS ====================

async def dungeon_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /dungeon command - Enter dungeon"""
    user_id = update.effective_user.id
    
    dungeon_id = create_dungeon(user_id)
    dungeon = get_dungeon(dungeon_id)
    
    await update.message.reply_text(
        dungeon.get_map_visual() + "\n\n"
        "Use /dungeonmove [up/down/left/right] to explore!",
        parse_mode=ParseMode.MARKDOWN
    )

async def dungeonmove_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /dungeonmove command"""
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text("❌ Usage: /dungeonmove [up/down/left/right]")
        return
    
    direction = context.args[0].lower()
    
    # Find user's dungeon
    for dungeon_id, dungeon in active_dungeons.items():
        if dungeon.player_id == user_id:
            result = dungeon.move(direction)
            
            text = dungeon.get_map_visual() + "\n\n"
            
            for event in result.get("events", []):
                if event["type"] == "encounter":
                    text += f"👹 You encountered a {event['monster'].name}!\n"
                    text += "Use /dungeonfight to battle!\n"
                elif event["type"] == "treasure":
                    text += f"💎 Found: {event['item']['name']}!\n"
                elif event["type"] == "trap":
                    text += f"💀 Trap! Lost {event['damage']} HP!\n"
                elif event["type"] == "exit":
                    text += f"🌟 {event['message']}\n"
            
            if result.get("game_over"):
                text += "\n💀 *GAME OVER*"
                end_dungeon(dungeon_id)
            
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
            return
    
    await update.message.reply_text("❌ No active dungeon! Start with /dungeon")

# ==================== API INTEGRATION COMMANDS ====================

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /weather command"""
    location = ' '.join(context.args) if context.args else "Your Location"
    
    weather = await api_service.get_weather(location)
    
    await update.message.reply_text(
        f"🌤️ *WEATHER IN {location.upper()}*\n═══════════════════\n\n"
        f"{weather['emoji']} {weather['condition'].title()}\n"
        f"🌡️ Temperature: {weather['temperature']}°C\n"
        f"💧 Humidity: {weather['humidity']}%\n"
        f"💨 Wind: {weather['wind_speed']} km/h",
        parse_mode=ParseMode.MARKDOWN
    )

async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /news command"""
    headlines = await api_service.get_news()
    
    text = "📰 *LATEST NEWS*\n═══════════════════\n\n"
    for headline in headlines:
        text += f"• {headline}\n\n"
    
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def stock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stock command"""
    if not context.args:
        # Show all stocks
        stocks = await api_service.get_all_stocks()
        
        text = "📈 *STOCK MARKET*\n═══════════════════\n\n"
        for symbol, stock in stocks.items():
            change_emoji = "📈" if stock["change"] >= 0 else "📉"
            text += f"{change_emoji} {symbol}: ${stock['price']:.2f} ({stock['change']:+.2f}%)\n"
    else:
        symbol = context.args[0].upper()
        stock = await api_service.get_stock_price(symbol)
        
        if stock:
            change_emoji = "📈" if stock["change"] >= 0 else "📉"
            text = (
                f"📈 *{stock['name']} ({stock['symbol']})*\n"
                f"═══════════════════\n\n"
                f"Price: ${stock['price']:.2f}\n"
                f"Change: {change_emoji} {stock['change']:+.2f}%"
            )
        else:
            text = "❌ Stock not found!"
    
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def fact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /fact command"""
    fact = await api_service.get_random_fact()
    await update.message.reply_text(fact)

# Import needed variables
from games.rpg_battle import active_battles
from games.casino import casino_games
from games.dungeon import active_dungeons
