from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class AdvisorRequest(BaseModel):
    hand: str
    stack: Optional[int] = None
    players: Optional[int] = None
    position: Optional[str] = None
    facing_bets: Optional[str] = None

class StreetState(BaseModel):
    hero_cards: list[str]
    board: list[str]
    street: str
    
    pot: float | None = None   # <-- REQUIRED FIX
    
    action: str | None = None
    opponents: int | None = 1
    facing_action: dict | None = None
    position: str | None = None



class PreflopState(BaseModel):
    hero_cards: list[str]
    position: str | None = None
    facing_bets: Optional[Dict[str, Any]] = None
