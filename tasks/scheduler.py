"""
Background Task Scheduler for Fam Tree Bot
===========================================
Handles scheduled tasks like daily resets, crop growth, etc.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Callable

logger = logging.getLogger(__name__)

class TaskScheduler:
    """Scheduler for background tasks"""
    
    def __init__(self):
        self.tasks = []
        self.running = False
    
    def add_task(self, func: Callable, interval: int, name: str = "task"):
        """Add a recurring task"""
        self.tasks.append({
            'func': func,
            'interval': interval,
            'name': name,
            'last_run': datetime.utcnow()
        })
        logger.info(f"Added task: {name} (interval: {interval}s)")
    
    async def run(self):
        """Run the scheduler loop"""
        self.running = True
        logger.info("Task scheduler started")
        
        while self.running:
            now = datetime.utcnow()
            
            for task in self.tasks:
                elapsed = (now - task['last_run']).total_seconds()
                if elapsed >= task['interval']:
                    try:
                        await task['func']()
                        task['last_run'] = now
                        logger.debug(f"Executed task: {task['name']}")
                    except Exception as e:
                        logger.error(f"Task {task['name']} failed: {e}")
            
            await asyncio.sleep(1)
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        logger.info("Task scheduler stopped")

# Global scheduler instance
scheduler = TaskScheduler()

# Task functions
async def reset_daily_limits():
    """Reset daily limits for all users"""
    from models.database import init_db_engine, get_session, User
    
    engine = init_db_engine()
    session = get_session(engine)
    
    try:
        users = session.query(User).all()
        for user in users:
            user.robbery_count_today = 0
            user.kill_count_today = 0
            user.last_reset_day = datetime.utcnow()
        session.commit()
        logger.info(f"Reset daily limits for {len(users)} users")
    except Exception as e:
        logger.error(f"Failed to reset daily limits: {e}")
    finally:
        session.close()

async def process_crop_growth():
    """Process crop growth and mark ready crops"""
    from models.database import init_db_engine, get_session, GardenPlot
    
    engine = init_db_engine()
    session = get_session(engine)
    
    try:
        plots = session.query(GardenPlot).filter_by(is_empty=False, is_ready=False).all()
        now = datetime.utcnow()
        updated = 0
        
        for plot in plots:
            if plot.planted_at and plot.growth_time:
                ready_time = plot.planted_at + timedelta(seconds=plot.growth_time)
                if now >= ready_time:
                    plot.is_ready = True
                    updated += 1
        
        session.commit()
        if updated > 0:
            logger.info(f"Marked {updated} crops as ready")
    except Exception as e:
        logger.error(f"Failed to process crop growth: {e}")
    finally:
        session.close()

async def check_worker_completions():
    """Check for completed worker tasks"""
    from models.database import init_db_engine, get_session, Worker
    
    engine = init_db_engine()
    session = get_session(engine)
    
    try:
        workers = session.query(Worker).filter_by(status='working').all()
        now = datetime.utcnow()
        completed = 0
        
        for worker in workers:
            if worker.work_end_time and now >= worker.work_end_time:
                worker.status = 'completed'
                completed += 1
        
        session.commit()
        if completed > 0:
            logger.info(f"Completed {completed} worker tasks")
    except Exception as e:
        logger.error(f"Failed to check worker completions: {e}")
    finally:
        session.close()

async def send_daily_reminders(bot):
    """Send daily reminders to users"""
    from models.database import init_db_engine, get_session, User
    
    engine = init_db_engine()
    session = get_session(engine)
    
    try:
        users = session.query(User).all()
        now = datetime.utcnow()
        
        for user in users:
            # Check if daily bonus not claimed
            if user.last_daily:
                time_since = now - user.last_daily
                if time_since >= timedelta(hours=20):  # Remind 4 hours before reset
                    try:
                        await bot.send_message(
                            chat_id=user.telegram_id,
                            text="⏰ *Daily Bonus Reminder*\n\n"
                                 "Don't forget to claim your daily bonus!\n"
                                 "Use /daily to claim now!",
                            parse_mode="Markdown"
                        )
                    except:
                        pass
    except Exception as e:
        logger.error(f"Failed to send reminders: {e}")
    finally:
        session.close()

async def cleanup_old_data():
    """Clean up old data and expired items"""
    from models.database import init_db_engine, get_session, MarketListing, GameSession
    
    engine = init_db_engine()
    session = get_session(engine)
    
    try:
        # Remove old inactive market listings
        old_listings = session.query(MarketListing).filter(
            MarketListing.listed_at < datetime.utcnow() - timedelta(days=7),
            MarketListing.is_active == False
        ).all()
        
        for listing in old_listings:
            session.delete(listing)
        
        # Remove old game sessions
        old_sessions = session.query(GameSession).filter(
            GameSession.started_at < datetime.utcnow() - timedelta(hours=24)
        ).all()
        
        for game in old_sessions:
            session.delete(game)
        
        session.commit()
        logger.info(f"Cleaned up {len(old_listings)} listings and {len(old_sessions)} game sessions")
    except Exception as e:
        logger.error(f"Failed to cleanup data: {e}")
    finally:
        session.close()

# Initialize tasks
def init_scheduler():
    """Initialize and start the scheduler"""
    # Add tasks with their intervals in seconds
    scheduler.add_task(reset_daily_limits, 86400, "daily_reset")  # Every 24 hours
    scheduler.add_task(process_crop_growth, 60, "crop_growth")     # Every minute
    scheduler.add_task(check_worker_completions, 60, "worker_check")  # Every minute
    scheduler.add_task(cleanup_old_data, 3600, "cleanup")          # Every hour
    
    return scheduler
