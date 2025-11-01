from quart import Blueprint, jsonify
from quart_schema import validate_querystring, document_response
from pydantic import BaseModel,Field
from typing import Optional, Dict

class TickerQuery(BaseModel):
    symbol: Optional[str] = Field(
        None,
        title="Trading Symbol",
        description='Trading pair, e.g., "BTC_USDT"'
    )
    limit: Optional[int] = Field(
        None,
        title="Limit",
        description="Number of tickers to return"
    )

class TickerInfo(BaseModel):
    ask: float = Field(..., example=110135.91)
    ask_volume: float = Field(..., example=1.35644)
    bid: float = Field(..., example=110135.9)
    bid_volume: float = Field(..., example=0.09895)
    last_update: int = Field(..., example=1761986671134)

class TickerResponse(BaseModel):
    binance: Dict[str, TickerInfo] = Field(
        ...,
        example={
            "BTC_USDT": {
                "ask": 110135.91,
                "ask_volume": 1.35644,
                "bid": 110135.9,
                "bid_volume": 0.09895,
                "last_update": 1761986671134
            },
            "ETH_USDT": {
                "ask": 3869.21,
                "ask_volume": 86.8358,
                "bid": 3869.2,
                "bid_volume": 6.8901,
                "last_update": 1761986671753
            }
        }
    )

def create_public_routes(ex_tracker):
   public_api = Blueprint("public_api", __name__)

   @public_api.get("/api")
   @validate_querystring(TickerQuery)
   @document_response(TickerResponse, status_code=200)
   async def ticker_all(query_args: TickerQuery):
      """
      Hello
      """
      data = ex_tracker.get_cache()
      return jsonify(data)
   
   return public_api