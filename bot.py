"""
Fam Tree Bot - Main Entry Point
================================
The Ultimate Telegram Family Simulation RPG Bot

Features:
- 200+ Commands across 40 modules
- Family Tree System
- Friend Circle Network
- Economy & Combat
- Garden/Farming Simulation
- Factory/Worker Management
- Trading Marketplace
- Mini Games
- AI Features
- Blockchain Integration
- And much more!

Bot Names:
- Alpha: @fam_tree_bot
- Beta: @famtreebbot

Version: 2.0.0
"""

import logging
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    InlineQueryHandler,
    filters,
    ContextTypes,
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Import configuration
from config.settings import BOT_TOKEN, LOG_LEVEL

# Import command handlers
from handlers.commands import (
    start_command, help_command,
    tree_command, adopt_command, marry_command, divorce_command, relations_command,
    friend_command, unfriend_command, circle_command, activefriends_command,
    account_command, bank_command, deposit_command, withdraw_command, pay_command,
    weapon_command, rob_command, kill_command, medical_command, donateblood_command, insurance_command,
)

from handlers.commands2 import (
    daily_command, fuse_command, reactions_command,
    factory_command, hire_command, fire_command,
    garden_command, plant_command, harvest_command, barn_command, add_command, sell_command, boost_command, refill_command,
    stands_command, putstand_command, stand_command, gift_command,
    cook_command, stove_command,
)

from handlers.commands3 import (
    fourpics_command, ripple_command, nation_command, question_command, lottery_command,
    whichai_command, ftrivia_command, paper_command, crabs_command, roulette_command, sonar_command,
    moneyboard_command, leaderboard_command, showstats_command, interactions_command,
)

from handlers.commands4 import (
    figlet_command, qotd_command, shibapic_command, foodpic_command,
    randomjoke_command, dadjoke_command, evilinsult_command, randomadvice_command,
    shorten_command, name2gender_command, name2nation_command, ip2loc_command,
    setlang_command, scope_command, toggle_command, autoprune_command, prune_command,
    waifu_command, waifus_command, setloc_command, showmap_command, wedcard_command,
    refer_command, block_command, unblock_command, blocklist_command,
)

from handlers.callbacks import handle_callback
from handlers.messages import handle_text_message, handle_photo, handle_sticker, handle_inline_query
from handlers.admin import (
    admin_command, admin_stats_command, broadcast_command, give_command, take_command,
    ban_command, unban_command, maintenance_command, logs_command,
)

from handlers.advanced_commands import (
    # AI Commands
    ai_command, aigen_command, smart_command,
    # Blockchain Commands
    nft_command, crypto_command, mint_command,
    # Clan Commands
    clan_command, clancreate_command, clanlist_command,
    # Quest Commands
    quest_command,
    # Achievement Commands
    achievements_command,
    # RPG Battle Commands
    battle_command, battleattack_command,
    # Casino Commands
    slots_command, blackjack_command, bjhit_command,
    # Dungeon Commands
    dungeon_command, dungeonmove_command,
    # API Commands
    weather_command, news_command, stock_command, fact_command,
)

# Import database
from models.database import init_db

def setup_handlers(application: Application):
    """Setup all command handlers"""
    
    # ==================== CORE COMMANDS ====================
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # ==================== MODULE 1: FAMILY COMMANDS ====================
    application.add_handler(CommandHandler("tree", tree_command))
    application.add_handler(CommandHandler("fulltree", tree_command))
    application.add_handler(CommandHandler("bloodtree", tree_command))
    application.add_handler(CommandHandler("adopt", adopt_command))
    application.add_handler(CommandHandler("marry", marry_command))
    application.add_handler(CommandHandler("divorce", divorce_command))
    application.add_handler(CommandHandler("disown", adopt_command))  # Reuse adopt handler
    application.add_handler(CommandHandler("runaway", adopt_command))  # Reuse adopt handler
    application.add_handler(CommandHandler("relations", relations_command))
    application.add_handler(CommandHandler("relation", relations_command))
    application.add_handler(CommandHandler("family", tree_command))
    application.add_handler(CommandHandler("makeparent", adopt_command))
    application.add_handler(CommandHandler("sibling", adopt_command))
    application.add_handler(CommandHandler("setpic", account_command))
    application.add_handler(CommandHandler("setpfp", account_command))
    application.add_handler(CommandHandler("customize", account_command))
    
    # ==================== MODULE 2: FRIEND COMMANDS ====================
    application.add_handler(CommandHandler("circle", circle_command))
    application.add_handler(CommandHandler("friends", circle_command))
    application.add_handler(CommandHandler("friend", friend_command))
    application.add_handler(CommandHandler("unfriend", unfriend_command))
    application.add_handler(CommandHandler("suggestions", circle_command))
    application.add_handler(CommandHandler("flink", circle_command))
    application.add_handler(CommandHandler("ratings", circle_command))
    application.add_handler(CommandHandler("activefriends", activefriends_command))
    application.add_handler(CommandHandler("fsearch", circle_command))
    
    # ==================== MODULE 3: ACCOUNT COMMANDS ====================
    application.add_handler(CommandHandler("account", account_command))
    application.add_handler(CommandHandler("profile", account_command))
    application.add_handler(CommandHandler("acc", account_command))
    application.add_handler(CommandHandler("me", account_command))
    application.add_handler(CommandHandler("bank", bank_command))
    application.add_handler(CommandHandler("deposit", deposit_command))
    application.add_handler(CommandHandler("withdraw", withdraw_command))
    application.add_handler(CommandHandler("pay", pay_command))
    application.add_handler(CommandHandler("weapon", weapon_command))
    application.add_handler(CommandHandler("rob", rob_command))
    application.add_handler(CommandHandler("kill", kill_command))
    application.add_handler(CommandHandler("medical", medical_command))
    application.add_handler(CommandHandler("donateblood", donateblood_command))
    application.add_handler(CommandHandler("insurance", insurance_command))
    application.add_handler(CommandHandler("reputation", account_command))
    application.add_handler(CommandHandler("skills", account_command))
    
    # ==================== MODULE 4: DAILY COMMANDS ====================
    application.add_handler(CommandHandler("daily", daily_command))
    application.add_handler(CommandHandler("fuse", fuse_command))
    application.add_handler(CommandHandler("reactions", reactions_command))
    application.add_handler(CommandHandler("rxns", reactions_command))
    application.add_handler(CommandHandler("addgif", reactions_command))
    application.add_handler(CommandHandler("showgifs", reactions_command))
    application.add_handler(CommandHandler("remgifs", reactions_command))
    
    # ==================== MODULE 5: FACTORY COMMANDS ====================
    application.add_handler(CommandHandler("factory", factory_command))
    application.add_handler(CommandHandler("hire", hire_command))
    application.add_handler(CommandHandler("fire", fire_command))
    application.add_handler(CommandHandler("buy", weapon_command))  # For buy shield/sword
    
    # ==================== MODULE 6: GARDEN COMMANDS ====================
    application.add_handler(CommandHandler("garden", garden_command))
    application.add_handler(CommandHandler("gardens", garden_command))
    application.add_handler(CommandHandler("add", add_command))
    application.add_handler(CommandHandler("adds", add_command))
    application.add_handler(CommandHandler("buys", add_command))
    application.add_handler(CommandHandler("purchase", add_command))
    application.add_handler(CommandHandler("plant", plant_command))
    application.add_handler(CommandHandler("plants", plant_command))
    application.add_handler(CommandHandler("harvest", harvest_command))
    application.add_handler(CommandHandler("sells", sell_command))
    application.add_handler(CommandHandler("sell", sell_command))
    application.add_handler(CommandHandler("barn", barn_command))
    application.add_handler(CommandHandler("bn", barn_command))
    application.add_handler(CommandHandler("boost", boost_command))
    application.add_handler(CommandHandler("refill", refill_command))
    application.add_handler(CommandHandler("track", garden_command))
    application.add_handler(CommandHandler("orders", garden_command))
    application.add_handler(CommandHandler("fertilise", garden_command))
    
    # ==================== MODULE 7: TRADING COMMANDS ====================
    application.add_handler(CommandHandler("stands", stands_command))
    application.add_handler(CommandHandler("putstand", putstand_command))
    application.add_handler(CommandHandler("stand", stand_command))
    application.add_handler(CommandHandler("gift", gift_command))
    application.add_handler(CommandHandler("alert", stands_command))
    
    # ==================== MODULE 8: COOKING COMMANDS ====================
    application.add_handler(CommandHandler("cook", cook_command))
    application.add_handler(CommandHandler("stove", stove_command))
    
    # ==================== MODULE 9: GAME COMMANDS ====================
    application.add_handler(CommandHandler("4p", fourpics_command))
    application.add_handler(CommandHandler("fourpics", fourpics_command))
    application.add_handler(CommandHandler("4h", fourpics_command))
    application.add_handler(CommandHandler("4w", fourpics_command))
    application.add_handler(CommandHandler("4s", fourpics_command))
    application.add_handler(CommandHandler("ripple", ripple_command))
    application.add_handler(CommandHandler("rbet", ripple_command))
    application.add_handler(CommandHandler("rtake", ripple_command))
    application.add_handler(CommandHandler("bets", ripple_command))
    application.add_handler(CommandHandler("nation", nation_command))
    application.add_handler(CommandHandler("question", question_command))
    application.add_handler(CommandHandler("lottery", lottery_command))
    application.add_handler(CommandHandler("whichai", whichai_command))
    application.add_handler(CommandHandler("ftrivia", ftrivia_command))
    application.add_handler(CommandHandler("paper", paper_command))
    application.add_handler(CommandHandler("crabs", crabs_command))
    application.add_handler(CommandHandler("roulette", roulette_command))
    application.add_handler(CommandHandler("sonar", sonar_command))
    
    # ==================== MODULE 10: STATS COMMANDS ====================
    application.add_handler(CommandHandler("mb", moneyboard_command))
    application.add_handler(CommandHandler("moneyboard", moneyboard_command))
    application.add_handler(CommandHandler("leaderboard", leaderboard_command))
    application.add_handler(CommandHandler("moneygraph", showstats_command))
    application.add_handler(CommandHandler("mg", showstats_command))
    application.add_handler(CommandHandler("showstats", showstats_command))
    application.add_handler(CommandHandler("loadstats", showstats_command))
    application.add_handler(CommandHandler("interactions", interactions_command))
    
    # ==================== MODULE 11: UTILITY COMMANDS ====================
    application.add_handler(CommandHandler("figlet", figlet_command))
    application.add_handler(CommandHandler("qotd", qotd_command))
    application.add_handler(CommandHandler("shibapic", shibapic_command))
    application.add_handler(CommandHandler("foodpic", foodpic_command))
    application.add_handler(CommandHandler("randomjoke", randomjoke_command))
    application.add_handler(CommandHandler("dadjoke", dadjoke_command))
    application.add_handler(CommandHandler("evilinsult", evilinsult_command))
    application.add_handler(CommandHandler("randomadvice", randomadvice_command))
    application.add_handler(CommandHandler("shorten", shorten_command))
    application.add_handler(CommandHandler("name2gender", name2gender_command))
    application.add_handler(CommandHandler("name2nation", name2nation_command))
    application.add_handler(CommandHandler("ip2loc", ip2loc_command))
    
    # ==================== MODULE 12: SETTINGS COMMANDS ====================
    application.add_handler(CommandHandler("setlang", setlang_command))
    application.add_handler(CommandHandler("scope", scope_command))
    application.add_handler(CommandHandler("toggle", toggle_command))
    application.add_handler(CommandHandler("autoprune", autoprune_command))
    application.add_handler(CommandHandler("prune", prune_command))
    application.add_handler(CommandHandler("disable", toggle_command))
    application.add_handler(CommandHandler("enable", toggle_command))
    application.add_handler(CommandHandler("disabled", toggle_command))
    application.add_handler(CommandHandler("gifs", toggle_command))
    application.add_handler(CommandHandler("incests", toggle_command))
    application.add_handler(CommandHandler("treemode", scope_command))
    
    # ==================== MODULE 13: EXTRA COMMANDS ====================
    application.add_handler(CommandHandler("waifu", waifu_command))
    application.add_handler(CommandHandler("waifus", waifus_command))
    application.add_handler(CommandHandler("waifugraph", waifus_command))
    application.add_handler(CommandHandler("setloc", setloc_command))
    application.add_handler(CommandHandler("setlocation", setloc_command))
    application.add_handler(CommandHandler("showmap", showmap_command))
    application.add_handler(CommandHandler("wedcard", wedcard_command))
    application.add_handler(CommandHandler("refer", refer_command))
    application.add_handler(CommandHandler("block", block_command))
    application.add_handler(CommandHandler("unblock", unblock_command))
    application.add_handler(CommandHandler("blocklist", blocklist_command))
    
    # ==================== ADMIN COMMANDS ====================
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("adminstats", admin_stats_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    application.add_handler(CommandHandler("give", give_command))
    application.add_handler(CommandHandler("take", take_command))
    application.add_handler(CommandHandler("ban", ban_command))
    application.add_handler(CommandHandler("unban", unban_command))
    application.add_handler(CommandHandler("maintenance", maintenance_command))
    application.add_handler(CommandHandler("logs", logs_command))
    
    # ==================== ADVANCED MODULES 21-40 ====================
    
    # Module 21: AI Features
    application.add_handler(CommandHandler("ai", ai_command))
    application.add_handler(CommandHandler("aigen", aigen_command))
    application.add_handler(CommandHandler("smart", smart_command))
    
    # Module 22: Blockchain
    application.add_handler(CommandHandler("nft", nft_command))
    application.add_handler(CommandHandler("crypto", crypto_command))
    application.add_handler(CommandHandler("mint", mint_command))
    
    # Module 28: Clan System
    application.add_handler(CommandHandler("clan", clan_command))
    application.add_handler(CommandHandler("guild", clan_command))
    application.add_handler(CommandHandler("clancreate", clancreate_command))
    application.add_handler(CommandHandler("clanlist", clanlist_command))
    application.add_handler(CommandHandler("clanjoin", clanlist_command))
    application.add_handler(CommandHandler("claninvite", clanlist_command))
    application.add_handler(CommandHandler("clankick", clanlist_command))
    application.add_handler(CommandHandler("clandonate", clanlist_command))
    application.add_handler(CommandHandler("clanwar", clanlist_command))
    application.add_handler(CommandHandler("alliance", clanlist_command))
    
    # Module 27: Achievements
    application.add_handler(CommandHandler("achievements", achievements_command))
    application.add_handler(CommandHandler("trophies", achievements_command))
    application.add_handler(CommandHandler("milestone", achievements_command))
    application.add_handler(CommandHandler("title", achievements_command))
    
    # Module 25: Advanced Games
    application.add_handler(CommandHandler("battle", battle_command))
    application.add_handler(CommandHandler("battleattack", battleattack_command))
    application.add_handler(CommandHandler("battleskill", battleattack_command))
    application.add_handler(CommandHandler("quest", quest_command))
    application.add_handler(CommandHandler("dungeon", dungeon_command))
    application.add_handler(CommandHandler("dungeonmove", dungeonmove_command))
    application.add_handler(CommandHandler("dungeonfight", dungeonmove_command))
    application.add_handler(CommandHandler("slots", slots_command))
    application.add_handler(CommandHandler("blackjack", blackjack_command))
    application.add_handler(CommandHandler("bjhit", bjhit_command))
    application.add_handler(CommandHandler("bjstand", bjhit_command))
    application.add_handler(CommandHandler("dice", slots_command))
    application.add_handler(CommandHandler("casino", slots_command))
    
    # Module 34: API Integrations
    application.add_handler(CommandHandler("weather", weather_command))
    application.add_handler(CommandHandler("news", news_command))
    application.add_handler(CommandHandler("stock", stock_command))
    application.add_handler(CommandHandler("fact", fact_command))
    
    # Module 26: Events
    application.add_handler(CommandHandler("events", quest_command))
    application.add_handler(CommandHandler("event", quest_command))
    application.add_handler(CommandHandler("seasonal", quest_command))
    
    # Module 31: Tournaments
    application.add_handler(CommandHandler("tournament", quest_command))
    application.add_handler(CommandHandler("compete", quest_command))
    application.add_handler(CommandHandler("championship", quest_command))
    
    # Module 29: Advanced Marketplace
    application.add_handler(CommandHandler("auction", quest_command))
    application.add_handler(CommandHandler("blackmarket", quest_command))
    application.add_handler(CommandHandler("stocks", stock_command))
    
    # ==================== CALLBACK HANDLER ====================
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    # ==================== MESSAGE HANDLERS ====================
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))
    
    # ==================== INLINE QUERY ====================
    application.add_handler(InlineQueryHandler(handle_inline_query))
    
    logger.info("All handlers registered successfully!")

def main():
    """Main function to start the bot"""
    
    # Initialize database
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized!")
    
    # Create application
    logger.info("Starting Fam Tree Bot...")
    
    # Check for token
    token = BOT_TOKEN
    if token == "YOUR_BOT_TOKEN_HERE":
        logger.error("Please set your BOT_TOKEN in config/settings.py or as environment variable!")
        print("\n" + "="*60)
        print("ERROR: Bot token not configured!")
        print("="*60)
        print("\nPlease set your bot token in one of these ways:")
        print("1. Set BOT_TOKEN environment variable")
        print("2. Edit config/settings.py and set BOT_TOKEN")
        print("\nGet your bot token from @BotFather on Telegram")
        print("="*60 + "\n")
        return
    
    application = Application.builder().token(token).build()
    
    # Setup handlers
    setup_handlers(application)
    
    # Start the bot
    logger.info("Bot is running! Press Ctrl+C to stop.")
    print("\n" + "="*60)
    print("🌳 FAM TREE BOT IS RUNNING! 🌳")
    print("="*60)
    print("\nBot Features:")
    print("  • 200+ Commands")
    print("  • Family Tree System")
    print("  • Friend Network")
    print("  • Economy & Combat")
    print("  • Garden/Farming")
    print("  • Factory Management")
    print("  • Trading Marketplace")
    print("  • Mini Games")
    print("  • And much more!")
    print("\nPress Ctrl+C to stop the bot")
    print("="*60 + "\n")
    
    # Run the bot until stopped
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
