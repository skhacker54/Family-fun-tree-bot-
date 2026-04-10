"""
Casino Games for Fam Tree Bot
==============================
Advanced casino game implementations
"""

import random
from typing import Dict, List, Tuple

class SlotMachine:
    """Slot machine game"""
    
    SYMBOLS = {
        "🍒": {"value": 2, "probability": 0.3},
        "🍋": {"value": 3, "probability": 0.25},
        "🍊": {"value": 4, "probability": 0.2},
        "🍇": {"value": 5, "probability": 0.15},
        "💎": {"value": 10, "probability": 0.08},
        "7️⃣": {"value": 50, "probability": 0.02},
    }
    
    @staticmethod
    def spin() -> Tuple[List[str], int, bool]:
        """Spin the slot machine"""
        symbols = list(SlotMachine.SYMBOLS.keys())
        weights = [SlotMachine.SYMBOLS[s]["probability"] for s in symbols]
        
        result = random.choices(symbols, weights=weights, k=3)
        
        # Check for wins
        if result[0] == result[1] == result[2]:
            # Jackpot - all three match
            multiplier = SlotMachine.SYMBOLS[result[0]]["value"]
            return result, multiplier, True
        elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
            # Two match
            return result, 2, True
        else:
            return result, 0, False
    
    @staticmethod
    def get_visual(result: List[str]) -> str:
        """Get slot machine visual"""
        return f"""
╔════════════════════════════════════╗
║         🎰 SLOT MACHINE            ║
╠════════════════════════════════════╣
║                                    ║
║    ┌─────┐  ┌─────┐  ┌─────┐     ║
║    │ {result[0]}  │  │ {result[1]}  │  │ {result[2]}  │     ║
║    └─────┘  └─────┘  └─────┘     ║
║                                    ║
╚════════════════════════════════════╝
"""

class Blackjack:
    """Blackjack game"""
    
    SUITS = ['♠️', '♥️', '♦️', '♣️']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    def __init__(self):
        self.deck = self._create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.game_over = False
    
    def _create_deck(self) -> List[Tuple[str, str]]:
        """Create a deck of cards"""
        deck = [(rank, suit) for suit in self.SUITS for rank in self.RANKS]
        random.shuffle(deck)
        return deck
    
    def deal(self):
        """Deal initial cards"""
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
    
    def _card_value(self, card: Tuple[str, str]) -> int:
        """Get card value"""
        rank = card[0]
        if rank in ['J', 'Q', 'K']:
            return 10
        elif rank == 'A':
            return 11
        else:
            return int(rank)
    
    def hand_value(self, hand: List[Tuple[str, str]]) -> int:
        """Calculate hand value"""
        value = sum(self._card_value(card) for card in hand)
        aces = sum(1 for card in hand if card[0] == 'A')
        
        # Adjust for aces
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        
        return value
    
    def hit(self) -> bool:
        """Player hits"""
        self.player_hand.append(self.deck.pop())
        if self.hand_value(self.player_hand) > 21:
            self.game_over = True
            return False
        return True
    
    def stand(self):
        """Player stands, dealer plays"""
        while self.hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())
        self.game_over = True
    
    def get_result(self) -> Dict:
        """Get game result"""
        player_value = self.hand_value(self.player_hand)
        dealer_value = self.hand_value(self.dealer_hand)
        
        if player_value > 21:
            return {"result": "lose", "reason": "Bust!", "player": player_value, "dealer": dealer_value}
        elif dealer_value > 21:
            return {"result": "win", "reason": "Dealer bust!", "player": player_value, "dealer": dealer_value}
        elif player_value > dealer_value:
            return {"result": "win", "reason": "Higher hand!", "player": player_value, "dealer": dealer_value}
        elif dealer_value > player_value:
            return {"result": "lose", "reason": "Dealer wins!", "player": player_value, "dealer": dealer_value}
        else:
            return {"result": "push", "reason": "Tie!", "player": player_value, "dealer": dealer_value}
    
    def get_visual(self, show_dealer: bool = False) -> str:
        """Get game visual"""
        dealer_cards = ' '.join([f"{c[0]}{c[1]}" for c in self.dealer_hand]) if show_dealer else f"{self.dealer_hand[0][0]}{self.dealer_hand[0][1]} 🂠"
        player_cards = ' '.join([f"{c[0]}{c[1]}" for c in self.player_hand])
        
        return f"""
╔════════════════════════════════════╗
║         🃏 BLACKJACK               ║
╠════════════════════════════════════╣
║  Dealer: {dealer_cards:<25} ║
║        ({self.hand_value(self.dealer_hand) if show_dealer else '?'})                       ║
║                                    ║
║  You:   {player_cards:<25} ║
║        ({self.hand_value(self.player_hand)})                       ║
╚════════════════════════════════════╝
"""

class DiceGame:
    """Dice betting game"""
    
    @staticmethod
    def roll() -> Tuple[int, int]:
        """Roll two dice"""
        return random.randint(1, 6), random.randint(1, 6)
    
    @staticmethod
    def get_visual(dice: Tuple[int, int]) -> str:
        """Get dice visual"""
        dice_faces = {
            1: ["┌─────┐", "│     │", "│  ●  │", "│     │", "└─────┘"],
            2: ["┌─────┐", "│ ●   │", "│     │", "│   ● │", "└─────┘"],
            3: ["┌─────┐", "│ ●   │", "│  ●  │", "│   ● │", "└─────┘"],
            4: ["┌─────┐", "│ ● ● │", "│     │", "│ ● ● │", "└─────┘"],
            5: ["┌─────┐", "│ ● ● │", "│  ●  │", "│ ● ● │", "└─────┘"],
            6: ["┌─────┐", "│ ● ● │", "│ ● ● │", "│ ● ● │", "└─────┘"],
        }
        
        d1 = dice_faces[dice[0]]
        d2 = dice_faces[dice[1]]
        
        visual = "╔════════════════════════════════════╗\n║           🎲 DICE ROLL             ║\n╠════════════════════════════════════╣\n║                                    ║\n"
        for i in range(5):
            visual += f"║   {d1[i]}  {d2[i]}   ║\n"
        visual += "║                                    ║\n"
        visual += f"║         Total: {sum(dice)}                   ║\n"
        visual += "╚════════════════════════════════════╝"
        
        return visual

# Active games storage
casino_games = {}

def create_game(game_type: str, user_id: int) -> str:
    """Create a new casino game"""
    game_id = f"{game_type}_{user_id}_{random.randint(1000, 9999)}"
    
    if game_type == "blackjack":
        game = Blackjack()
        game.deal()
        casino_games[game_id] = {"type": "blackjack", "game": game}
    
    return game_id

def get_game(game_id: str) -> Dict:
    """Get active game"""
    return casino_games.get(game_id)

def end_game(game_id: str):
    """End a game"""
    if game_id in casino_games:
        del casino_games[game_id]
