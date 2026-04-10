"""
Blockchain Service for Fam Tree Bot
====================================
NFT and cryptocurrency integration
"""

import random
import hashlib
from datetime import datetime
from typing import Dict, List, Optional

class BlockchainService:
    """Blockchain service for NFTs and crypto features"""
    
    NFT_BADGES = {
        "founder": {"name": "Founder Badge", "rarity": "legendary", "description": "Early adopter of Fam Tree Bot"},
        "diamond_hands": {"name": "Diamond Hands", "rarity": "epic", "description": "Held assets for 1 year"},
        "royal_family": {"name": "Royal Family", "rarity": "legendary", "description": "100+ family members"},
        "super_farmer": {"name": "Super Farmer", "rarity": "epic", "description": "Maxed out garden"},
        "battle_master": {"name": "Battle Master", "rarity": "rare", "description": "100 PvP victories"},
        "wealthy": {"name": "Wealthy", "rarity": "rare", "description": "Earned $1,000,000"},
        "collector": {"name": "Collector", "rarity": "common", "description": "Collected 50 items"},
        "socialite": {"name": "Socialite", "rarity": "common", "description": "100 friends"},
    }
    
    @staticmethod
    def generate_nft_token_id(user_id: int, badge_type: str) -> str:
        """Generate unique NFT token ID"""
        data = f"{user_id}:{badge_type}:{datetime.utcnow().timestamp()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    @staticmethod
    def mint_badge(user_id: int, badge_type: str) -> Optional[Dict]:
        """Mint a new NFT badge"""
        if badge_type not in BlockchainService.NFT_BADGES:
            return None
        
        badge = BlockchainService.NFT_BADGES[badge_type].copy()
        badge["token_id"] = BlockchainService.generate_nft_token_id(user_id, badge_type)
        badge["owner_id"] = user_id
        badge["minted_at"] = datetime.utcnow().isoformat()
        badge["blockchain"] = "Polygon"
        
        return badge
    
    @staticmethod
    def get_user_nfts(user_id: int) -> List[Dict]:
        """Get user's NFT collection"""
        # Simulated NFT data
        nfts = []
        for badge_type, badge_info in BlockchainService.NFT_BADGES.items():
            if random.random() < 0.3:  # 30% chance user has each badge
                nft = BlockchainService.mint_badge(user_id, badge_type)
                if nft:
                    nfts.append(nft)
        return nfts
    
    @staticmethod
    def calculate_nft_value(nft: Dict) -> float:
        """Calculate NFT value in USD"""
        rarity_values = {
            "common": 10,
            "rare": 50,
            "epic": 200,
            "legendary": 1000,
        }
        return rarity_values.get(nft.get("rarity", "common"), 10)
    
    @staticmethod
    def crypto_to_usd(crypto_amount: float, currency: str = "ETH") -> float:
        """Convert crypto to USD (simulated rates)"""
        rates = {
            "BTC": 45000,
            "ETH": 3000,
            "SOL": 100,
            "USDT": 1,
        }
        return crypto_amount * rates.get(currency, 0)
    
    @staticmethod
    def create_smart_contract(contract_type: str, parties: List[int], terms: Dict) -> Dict:
        """Create a smart contract"""
        contract = {
            "contract_id": hashlib.sha256(f"{contract_type}:{parties}:{datetime.utcnow()}".encode()).hexdigest()[:20],
            "type": contract_type,
            "parties": parties,
            "terms": terms,
            "created_at": datetime.utcnow().isoformat(),
            "status": "active",
            "blockchain": "Ethereum",
        }
        return contract

# Global blockchain service instance
blockchain_service = BlockchainService()
