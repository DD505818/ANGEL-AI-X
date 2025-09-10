from pydantic import BaseModel, Field
class KillReq(BaseModel): enabled: bool
class OrderReq(BaseModel):
    client_order_id: str = Field(min_length=8)
    symbol: str
    side: str  # BUY/SELL
    qty: float
    price: float|None = None
class Portfolio(BaseModel):
    equity: float
    positions: list[dict]
