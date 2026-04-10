"""
Authentication & Authorization Middleware
==========================================
Handles user authentication, rate limiting, and access control
"""

import functools
import time
from datetime import datetime, timedelta
from typing import Callable, Optional
from telegram import Update
from telegram.ext import ContextTypes

from models.database import get_session, init_db_engine, User

# Rate limiting storage
rate_limit_store = {}

def rate_limit(max_calls: int = 10, window: int = 60):
    """Rate limit decorator for commands"""
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            user_id = update.effective_user.id
            current_time = time.time()
            
            # Initialize user's rate limit data
            if user_id not in rate_limit_store:
                rate_limit_store[user_id] = []
            
            # Clean old entries
            rate_limit_store[user_id] = [
                t for t in rate_limit_store[user_id] 
                if current_time - t < window
            ]
            
            # Check rate limit
            if len(rate_limit_store[user_id]) >= max_calls:
                await update.message.reply_text(
                    f"⏰ *Rate Limit Exceeded*\n\n"
                    f"Please wait {window} seconds before using this command again.",
                    parse_mode="Markdown"
                )
                return
            
            # Add current call
            rate_limit_store[user_id].append(current_time)
            
            return await func(update, context, *args, **kwargs)
        return wrapper
    return decorator

def require_registration(func: Callable):
    """Decorator to ensure user is registered"""
    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        engine = init_db_engine()
        session = get_session(engine)
        
        try:
            user = session.query(User).filter_by(telegram_id=update.effective_user.id).first()
            if not user:
                await update.message.reply_text(
                    "❌ *Not Registered*\n\n"
                    "Please use /start to register first!",
                    parse_mode="Markdown"
                )
                return
            
            # Update last active
            user.last_active = datetime.utcnow()
            session.commit()
            
            return await func(update, context, *args, **kwargs)
        finally:
            session.close()
    return wrapper

def admin_only(func: Callable):
    """Decorator for admin-only commands"""
    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        from config.settings import ADMIN_USER_IDS
        
        if update.effective_user.id not in ADMIN_USER_IDS:
            await update.message.reply_text(
                "🚫 *Access Denied*\n\n"
                "This command is for administrators only.",
                parse_mode="Markdown"
            )
            return
        
        return await func(update, context, *args, **kwargs)
    return wrapper

def cooldown(seconds: int = 60):
    """Cooldown decorator for commands"""
    cooldowns = {}
    
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            user_id = update.effective_user.id
            current_time = time.time()
            
            if user_id in cooldowns:
                time_passed = current_time - cooldowns[user_id]
                if time_passed < seconds:
                    remaining = int(seconds - time_passed)
                    await update.message.reply_text(
                        f"⏳ *Cooldown Active*\n\n"
                        f"Please wait {remaining} seconds before using this command again.",
                        parse_mode="Markdown"
                    )
                    return
            
            cooldowns[user_id] = current_time
            return await func(update, context, *args, **kwargs)
        return wrapper
    return decorator

def log_command(func: Callable):
    """Decorator to log command usage"""
    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        command = update.message.text.split()[0] if update.message else "callback"
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
              f"User: @{user.username or user.id} | Command: {command}")
        
        return await func(update, context, *args, **kwargs)
    return wrapper
