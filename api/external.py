"""
External API Integrations for Fam Tree Bot
===========================================
Weather, news, stocks, translation APIs
"""

import aiohttp
import random
from typing import Dict, Optional

class ExternalAPIService:
    """Service for external API integrations"""
    
    # Simulated weather data
    WEATHER_CONDITIONS = {
        "sunny": {"emoji": "☀️", "temp_range": (20, 35)},
        "cloudy": {"emoji": "☁️", "temp_range": (15, 25)},
        "rainy": {"emoji": "🌧️", "temp_range": (10, 20)},
        "snowy": {"emoji": "❄️", "temp_range": (-5, 5)},
        "stormy": {"emoji": "⛈️", "temp_range": (15, 25)},
    }
    
    # Simulated news headlines
    NEWS_HEADLINES = [
        "🌾 Global crop prices surge as demand increases",
        "💰 New cryptocurrency regulation announced",
        "🏆 Annual Family Tree Championship begins",
        "🎮 New dungeon discovered in virtual world",
        "🌟 Rare gemstone found in player's garden",
        "⚔️ Epic clan war ends in dramatic victory",
        "🎁 Special holiday event announced",
        "🚀 New features coming to Fam Tree Bot",
    ]
    
    # Simulated stock prices
    STOCKS = {
        "CORN": {"name": "Corn Corp", "price": 45.50, "change": 2.3},
        "WHT": {"name": "Wheat Inc", "price": 32.75, "change": -1.2},
        "TOM": {"name": "Tomato Farms", "price": 28.90, "change": 5.1},
        "POT": {"name": "Potato Co", "price": 18.25, "change": 0.8},
    }
    
    @staticmethod
    async def get_weather(location: str) -> Dict:
        """Get weather for location (simulated)"""
        condition = random.choice(list(ExternalAPIService.WEATHER_CONDITIONS.keys()))
        data = ExternalAPIService.WEATHER_CONDITIONS[condition]
        temp = random.randint(*data["temp_range"])
        
        return {
            "location": location,
            "condition": condition,
            "emoji": data["emoji"],
            "temperature": temp,
            "humidity": random.randint(30, 90),
            "wind_speed": random.randint(0, 30),
        }
    
    @staticmethod
    async def get_news(category: str = "general") -> List[str]:
        """Get news headlines (simulated)"""
        return random.sample(ExternalAPIService.NEWS_HEADLINES, min(3, len(ExternalAPIService.NEWS_HEADLINES)))
    
    @staticmethod
    async def get_stock_price(symbol: str) -> Optional[Dict]:
        """Get stock price (simulated)"""
        stock = ExternalAPIService.STOCKS.get(symbol.upper())
        if stock:
            # Simulate price movement
            change_pct = random.uniform(-5, 5)
            new_price = stock["price"] * (1 + change_pct / 100)
            return {
                "symbol": symbol.upper(),
                "name": stock["name"],
                "price": round(new_price, 2),
                "change": round(change_pct, 2),
            }
        return None
    
    @staticmethod
    async def get_all_stocks() -> Dict:
        """Get all stock prices"""
        result = {}
        for symbol in ExternalAPIService.STOCKS:
            stock = await ExternalAPIService.get_stock_price(symbol)
            if stock:
                result[symbol] = stock
        return result
    
    @staticmethod
    def translate_text(text: str, target_lang: str) -> str:
        """Simple translation (simulated)"""
        translations = {
            "es": {"hello": "hola", "family": "familia", "tree": "árbol"},
            "fr": {"hello": "bonjour", "family": "famille", "tree": "arbre"},
            "de": {"hello": "hallo", "family": "familie", "tree": "baum"},
            "ru": {"hello": "привет", "family": "семья", "tree": "дерево"},
            "zh": {"hello": "你好", "family": "家庭", "tree": "树"},
            "ja": {"hello": "こんにちは", "family": "家族", "tree": "木"},
        }
        
        lang_dict = translations.get(target_lang, {})
        words = text.lower().split()
        translated = [lang_dict.get(word, word) for word in words]
        return " ".join(translated)
    
    @staticmethod
    async def get_random_fact() -> str:
        """Get random fact"""
        facts = [
            "🌳 Did you know? The oldest family tree traces back over 2,000 years!",
            "💰 The first coin was minted over 2,600 years ago in Lydia.",
            "🌱 Corn was first domesticated in Mexico about 9,000 years ago.",
            "⚔️ The longest war in history lasted 335 years between the Netherlands and the Isles of Scilly.",
            "💎 Diamonds are formed under extreme pressure about 100 miles below Earth's surface.",
            "🏰 The Great Wall of China is over 13,000 miles long.",
            "🎮 The first video game was created in 1958.",
        ]
        return random.choice(facts)
    
    @staticmethod
    async def get_quote() -> Dict:
        """Get inspirational quote"""
        quotes = [
            {"text": "The family is one of nature's masterpieces.", "author": "George Santayana"},
            {"text": "Family is not an important thing. It's everything.", "author": "Michael J. Fox"},
            {"text": "In every conceivable manner, the family is link to our past, bridge to our future.", "author": "Alex Haley"},
            {"text": "The love of family and the admiration of friends is much more important than wealth and privilege.", "author": "Charles Kuralt"},
        ]
        return random.choice(quotes)

# Global API service instance
api_service = ExternalAPIService()
