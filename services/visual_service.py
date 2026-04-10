"""
Visual Generation Service for Fam Tree Bot
===========================================
Generate ASCII art, charts, and visual representations
"""

import random
from datetime import datetime
from typing import Dict, List, Optional

class VisualService:
    """Service for generating visual content"""
    
    @staticmethod
    def generate_family_tree_ascii(user_name: str, partners: List[str], children: List[str], 
                                    parents: List[str], siblings: List[str]) -> str:
        """Generate ASCII family tree"""
        tree = f"""
╔══════════════════════════════════════════════════════════════╗
║                    🌳 FAMILY TREE                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║                        ┌─────────┐                          ║
║                        │   👤    │                          ║
║                        │ {user_name[:10]:^10}│                          ║
║                        └────┬────┘                          ║
║                             │                               ║
║            ┌────────────────┼────────────────┐              ║
║            │                │                │              ║
║       ┌────┴────┐     ┌────┴────┐     ┌────┴────┐         ║
║       │  💍     │     │  👶     │     │  👨‍👩   │         ║
║       │Partners │     │ Children│     │ Parents │         ║
║       │  {len(partners):^3}     │     │   {len(children):^3}   │     │   {len(parents):^3}   │         ║
║       └─────────┘     └─────────┘     └─────────┘         ║
║                                                              ║
║  💍 Partners: {', '.join(partners[:3]) if partners else 'None':<35} ║
║  👶 Children: {', '.join(children[:3]) if children else 'None':<35} ║
║  👨‍👩 Parents: {', '.join(parents[:2]) if parents else 'None':<35} ║
║  👫 Siblings: {', '.join(siblings[:3]) if siblings else 'None':<35} ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        return tree
    
    @staticmethod
    def generate_garden_visual(plots: List[Dict], season: str) -> str:
        """Generate visual garden representation"""
        season_emojis = {
            "spring": "🌸", "summer": "☀️", "autumn": "🍂", "winter": "❄️"
        }
        
        crop_emojis = {
            "empty": "🟫", "growing": "🌱", "pepper": "🌶️", "potato": "🥔",
            "eggplant": "🍆", "carrot": "🥕", "corn": "🌽", "tomato": "🍅"
        }
        
        visual = f"""
╔══════════════════════════════════════════════════════════════╗
║              🌱 YOUR GARDEN - {season_emojis.get(season, '🌿')} {season.upper()}              ║
╠══════════════════════════════════════════════════════════════╣
"""
        
        # Create 3x3 grid
        for i in range(0, 9, 3):
            row = "║  "
            for j in range(3):
                idx = i + j
                if idx < len(plots):
                    plot = plots[idx]
                    if plot.get('is_empty'):
                        emoji = crop_emojis['empty']
                        status = "Empty"
                    elif plot.get('is_ready'):
                        emoji = crop_emojis.get(plot.get('crop_type'), '🌿')
                        status = "Ready!"
                    else:
                        emoji = crop_emojis['growing']
                        status = f"{plot.get('remaining', 0)}m"
                    row += f"┌─────┐ "
                else:
                    row += f"       "
            row += " ║\n║  "
            
            for j in range(3):
                idx = i + j
                if idx < len(plots):
                    plot = plots[idx]
                    if plot.get('is_empty'):
                        emoji = crop_emojis['empty']
                    elif plot.get('is_ready'):
                        emoji = crop_emojis.get(plot.get('crop_type'), '🌿')
                    else:
                        emoji = crop_emojis['growing']
                    row += f"│ {emoji} │ "
                else:
                    row += f"       "
            row += " ║\n║  "
            
            for j in range(3):
                idx = i + j
                if idx < len(plots):
                    plot = plots[idx]
                    if plot.get('is_empty'):
                        status = "Empty"
                    elif plot.get('is_ready'):
                        status = "Ready"
                    else:
                        status = f"{plot.get('remaining', 0)//60}h"
                    row += f"│{status:^5}│ "
                else:
                    row += f"       "
            row += " ║\n║  "
            
            for j in range(3):
                idx = i + j
                if idx < len(plots):
                    row += f"└─────┘ "
                else:
                    row += f"       "
            row += " ║"
            visual += row + "\n║                                                              ║\n"
        
        visual += """╚══════════════════════════════════════════════════════════════╝
         🟫 = Empty | 🌱 = Growing | 🌶️🥔🍆🥕🌽🍅 = Ready
"""
        return visual
    
    @staticmethod
    def generate_money_chart(user_data: Dict) -> str:
        """Generate ASCII money chart"""
        balance = user_data.get('balance', 0)
        bank = user_data.get('bank_balance', 0)
        total = balance + bank
        
        if total == 0:
            total = 1  # Avoid division by zero
        
        wallet_pct = int((balance / total) * 20)
        bank_pct = int((bank / total) * 20)
        
        chart = f"""
╔══════════════════════════════════════════════════════════════╗
║                    📊 MONEY DISTRIBUTION                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  💰 Wallet:  {'█' * wallet_pct}{'░' * (20 - wallet_pct)} {format_money(balance):>12} ║
║  🏦 Bank:    {'█' * bank_pct}{'░' * (20 - bank_pct)} {format_money(bank):>12} ║
║                                                              ║
║  💵 Total:   {'█' * 20} {format_money(total):>12} ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        return chart
    
    @staticmethod
    def generate_factory_visual(workers: List[Dict], rating: int) -> str:
        """Generate factory visual"""
        visual = f"""
╔══════════════════════════════════════════════════════════════╗
║                    🏭 FACTORY DASHBOARD                      ║
║                    ⭐ Rating: {rating:<4}                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║     🏭         ⚙️         ⚙️         ⚙️         🏭            ║
║    ╱╲        ╱╲        ╱╲        ╱╲        ╱╲             ║
║   ╱  ╲      ╱  ╲      ╱  ╲      ╱  ╲      ╱  ╲            ║
║  ╱ 🏭 ╲    ╱ 👷 ╲    ╱ 👷 ╲    ╱ 👷 ╲    ╱ 🏭 ╲           ║
║ ╱______╲  ╱______╲  ╱______╲  ╱______╲  ╱______╲          ║
║                                                              ║
║  Workers: {len(workers)}/5                                          ║
"""
        for i, worker in enumerate(workers[:5], 1):
            status = worker.get('status', 'idle')
            status_emoji = {'idle': '⚪', 'working': '🟡', 'completed': '🟢'}.get(status, '⚪')
            visual += f"║  {i}. @{worker.get('username', 'Unknown')[:12]:<12} [{status_emoji}] {status.upper():<10} ║\n"
        
        visual += """║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        return visual
    
    @staticmethod
    def generate_leaderboard_visual(users: List[Dict], title: str) -> str:
        """Generate visual leaderboard"""
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        
        visual = f"""
╔══════════════════════════════════════════════════════════════╗
║                    {title:^50} ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
"""
        for i, user in enumerate(users[:10], 1):
            medal = medals[i-1] if i <= 10 else f"{i}."
            username = user.get('username', 'Unknown')[:12]
            value = format_money(user.get('balance', 0))
            visual += f"║  {medal} {username:<15} {value:>20}          ║\n"
        
        visual += """║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        return visual
    
    @staticmethod
    def generate_weapon_arsenal(current_weapon: str) -> str:
        """Generate visual weapon arsenal"""
        weapons = {
            "punch": "👊", "blade": "🔪", "sword": "⚔️", "pistol": "🔫",
            "gun": "🔫", "bow": "🏹", "poison": "☠️", "rocket_launcher": "🚀"
        }
        
        visual = f"""
╔══════════════════════════════════════════════════════════════╗
║                    🔫 WEAPON ARSENAL                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   👊 Punch     {'✅' if current_weapon == 'punch' else '⬜'}  Free      Rob: 50   Kill: 50   ║
║   🔪 Blade     {'✅' if current_weapon == 'blade' else '⬜'}  $100      Rob: 80   Kill: 100  ║
║   ⚔️ Sword     {'✅' if current_weapon == 'sword' else '⬜'}  $200      Rob: 100  Kill: 150  ║
║   🔫 Pistol    {'✅' if current_weapon == 'pistol' else '⬜'}  $400      Rob: 160  Kill: 200  ║
║   🔫 Gun       {'✅' if current_weapon == 'gun' else '⬜'}  $500      Rob: 200  Kill: 200  ║
║   🏹 Bow       {'✅' if current_weapon == 'bow' else '⬜'}  $5,000    Rob: 300  Kill: 100  ║
║   ☠️ Poison    {'✅' if current_weapon == 'poison' else '⬜'}  $8,000    Rob: 400  Kill: 200  ║
║   🚀 Rocket    {'✅' if current_weapon == 'rocket_launcher' else '⬜'}  $10,000   Rob: 500  Kill: 200  ║
║                                                              ║
║   Current: {weapons.get(current_weapon, '👊')} {current_weapon.upper()}                                    ║
╚══════════════════════════════════════════════════════════════╝
"""
        return visual

# Helper function for formatting
def format_money(amount: float) -> str:
    return f"${amount:,.0f}"

# Global visual service instance
visual_service = VisualService()
