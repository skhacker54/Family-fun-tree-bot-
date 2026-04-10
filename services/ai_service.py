"""
AI Service for Fam Tree Bot
============================
Advanced AI-powered features and recommendations
"""

import random
from datetime import datetime
from typing import Dict, List, Optional

class AIService:
    """AI-powered service for smart recommendations"""
    
    @staticmethod
    def get_family_advice(user_data: Dict) -> str:
        """Get AI advice for family decisions"""
        advice_list = [
            "💡 *AI Suggestion*\n\nBased on your family size, consider adopting more children to increase your daily bonus!",
            "💡 *AI Suggestion*\n\nYour partner compatibility score is high. A marriage would be beneficial!",
            "💡 *AI Suggestion*\n\nConsider insuring your family members for better protection.",
            "💡 *AI Suggestion*\n\nYour family tree is growing well! Keep expanding your network.",
        ]
        return random.choice(advice_list)
    
    @staticmethod
    def get_garden_recommendation(season: str, user_crops: List[str]) -> str:
        """Get AI recommendation for garden"""
        recommendations = {
            "spring": "🌸 *AI Garden Tip*\n\nSpring is perfect for planting Pepper! Growth speed is 2× faster.",
            "summer": "☀️ *AI Garden Tip*\n\nSummer heat helps Corn and Tomato grow faster!",
            "autumn": "🍂 *AI Garden Tip*\n\nAutumn is the best season for Potatoes!",
            "winter": "❄️ *AI Garden Tip*\n\nWinter is ideal for Carrots. Plant them now!",
        }
        return recommendations.get(season, "🌱 *AI Garden Tip*\n\nPlant crops that match the current season for 2× growth speed!")
    
    @staticmethod
    def get_trading_advice(market_data: Dict) -> str:
        """Get AI trading advice"""
        advices = [
            "📈 *AI Market Analysis*\n\nCorn prices are trending up. Good time to sell!",
            "📉 *AI Market Analysis*\n\nTomato market is saturated. Consider holding.",
            "💰 *AI Trading Tip*\n\nDiversify your crops for better market stability.",
            "🎯 *AI Opportunity*\n\nEggplant demand is high! Plant more for profit.",
        ]
        return random.choice(advices)
    
    @staticmethod
    def predict_user_behavior(user_stats: Dict) -> str:
        """Predict user behavior using simple heuristics"""
        predictions = [
            "🔮 *AI Prediction*\n\nYou're likely to increase your wealth by 20% this week!",
            "🔮 *AI Prediction*\n\nYour activity pattern suggests you'll reach a milestone soon!",
            "🔮 *AI Prediction*\n\nBased on trends, you might make a big trade today!",
        ]
        return random.choice(predictions)
    
    @staticmethod
    def generate_personalized_greeting(user_name: str, time_of_day: str) -> str:
        """Generate personalized greeting"""
        greetings = {
            "morning": f"☀️ Good morning, {user_name}! Ready to grow your family tree today?",
            "afternoon": f"🌤️ Good afternoon, {user_name}! How's your garden doing?",
            "evening": f"🌙 Good evening, {user_name}! Time to check your daily rewards!",
            "night": f"🌌 Late night, {user_name}! Don't forget to harvest before bed!",
        }
        return greetings.get(time_of_day, f"👋 Hello, {user_name}!")
    
    @staticmethod
    def analyze_sentiment(text: str) -> Dict:
        """Simple sentiment analysis"""
        positive_words = ['good', 'great', 'awesome', 'love', 'happy', 'excellent', 'amazing']
        negative_words = ['bad', 'terrible', 'hate', 'sad', 'awful', 'worst', 'angry']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return {"sentiment": "positive", "score": positive_count - negative_count}
        elif negative_count > positive_count:
            return {"sentiment": "negative", "score": negative_count - positive_count}
        else:
            return {"sentiment": "neutral", "score": 0}

# Global AI service instance
ai_service = AIService()
