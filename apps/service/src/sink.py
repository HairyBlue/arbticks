__all__ = ("SinkTicker")

from arbticks_types.type_sink import TypeTickerSink
from datetime import datetime

class SinkTicker():
   def __init__(self) -> None:
      self.ticker_sink: TypeTickerSink = {}


   def sink(self, symbol: str, ask: float, ask_volume: float, bid: float, bid_volume: float):
      self.ticker_sink[symbol] = {
         "ask": ask,
         "ask_volume": ask_volume,
         "bid": bid,
         "bid_volume": bid_volume,
         "last_update": int(datetime.utcnow().timestamp() * 1000)
      }

   def get_ticker_sink(self):
      return self.ticker_sink