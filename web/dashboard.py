"""
Web Dashboard for Fam Tree Bot
===============================
Flask-based web interface for bot management
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime
import os

app = Flask(__name__)

class WebDashboard:
    """Web dashboard for bot statistics"""
    
    def __init__(self, bot_instance=None):
        self.bot = bot_instance
        self.app = app
    
    def get_stats(self) -> dict:
        """Get bot statistics"""
        from models.database import init_db_engine, get_session, User
        from sqlalchemy import func
        
        engine = init_db_engine()
        session = get_session(engine)
        
        try:
            total_users = session.query(User).count()
            total_money = session.query(func.sum(User.balance)).scalar() or 0
            total_bank = session.query(func.sum(User.bank_balance)).scalar() or 0
            
            # Get recent users
            recent_users = session.query(User).order_by(User.created_at.desc()).limit(5).all()
            
            return {
                "total_users": total_users,
                "total_money": total_money,
                "total_bank": total_bank,
                "recent_users": [
                    {
                        "username": u.username,
                        "balance": u.balance,
                        "created_at": u.created_at.isoformat() if u.created_at else None
                    }
                    for u in recent_users
                ],
                "timestamp": datetime.utcnow().isoformat()
            }
        finally:
            session.close()
    
    def run(self, host='0.0.0.0', port=5000):
        """Run the web server"""
        self.app.run(host=host, port=port, debug=False)

# Flask routes
@app.route('/')
def index():
    """Main dashboard page"""
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Fam Tree Bot Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 0;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            color: white;
            padding: 40px 0;
        }
        .header h1 {
            font-size: 3em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .stat-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-align: center;
            transition: transform 0.3s;
        }
        .stat-card:hover {
            transform: translateY(-5px);
        }
        .stat-icon {
            font-size: 3em;
            margin-bottom: 10px;
        }
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #333;
        }
        .stat-label {
            color: #666;
            font-size: 1.1em;
        }
        .footer {
            text-align: center;
            color: white;
            padding: 20px;
            margin-top: 40px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌳 Fam Tree Bot Dashboard</h1>
            <p>The Ultimate Telegram Family Simulation RPG</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">👥</div>
                <div class="stat-value" id="total-users">-</div>
                <div class="stat-label">Total Users</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💰</div>
                <div class="stat-value" id="total-money">-</div>
                <div class="stat-label">Total Money</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🏦</div>
                <div class="stat-value" id="total-bank">-</div>
                <div class="stat-label">Bank Deposits</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">⚡</div>
                <div class="stat-value" id="status">Online</div>
                <div class="stat-label">Bot Status</div>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2024 Fam Tree Bot | Version 2.0.0</p>
        </div>
    </div>
    
    <script>
        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                
                document.getElementById('total-users').textContent = data.total_users.toLocaleString();
                document.getElementById('total-money').textContent = '$' + data.total_money.toLocaleString();
                document.getElementById('total-bank').textContent = '$' + data.total_bank.toLocaleString();
            } catch (e) {
                console.error('Failed to load stats:', e);
            }
        }
        
        loadStats();
        setInterval(loadStats, 30000);  // Refresh every 30 seconds
    </script>
</body>
</html>
    """
    return html

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    dashboard = WebDashboard()
    return jsonify(dashboard.get_stats())

@app.route('/api/users')
def api_users():
    """API endpoint for user list"""
    from models.database import init_db_engine, get_session, User
    
    engine = init_db_engine()
    session = get_session(engine)
    
    try:
        users = session.query(User).limit(100).all()
        return jsonify([{
            "id": u.telegram_id,
            "username": u.username,
            "balance": u.balance,
            "reputation": u.reputation
        } for u in users])
    finally:
        session.close()

# Export dashboard
dashboard = WebDashboard()

def start_dashboard(host='0.0.0.0', port=5000):
    """Start the web dashboard"""
    dashboard.run(host, port)
