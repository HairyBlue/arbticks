import asyncio
import ccxt.pro as ccxt
from typing import Literal, Type
from arbticks_utils import supported_pairs
from arbticks_types.type_tickers import TypeTicker, TypeTickerInfo, TypeTickerMap

from sink import SinkTicker

ExchangeName = Literal["binance", "kraken"]

exchange_supported: dict[ExchangeName, Type[ccxt.Exchange]] = {
   "binance": ccxt.binance,
   "kraken": ccxt.bybit,
}

class ExchangeManager():
   def __init__(self, ex_name: ExchangeName) -> None:
      self._enable_watcher = True
      self.exchange = None

      self.ex_name = ex_name
      if exchange_supported[ex_name] is not None:
         self.exchange = exchange_supported[ex_name]()

   def _handle_tickers(self, ticker_map: TypeTickerMap) -> None:
      sink_ticker = SinkTicker()
      for symbol, value in ticker_map.items():
         ask = value["ask"]
         ask_volume = value["askVolume"]
         bid = value["bid"]
         bid_volume = value["bidVolume"]

         sink_ticker.sink(symbol, ask, ask_volume, bid, bid_volume)

   async def _watchers(self) -> None:
      while self._enable_watcher:
         out = await self.exchange.watch_tickers(list(supported_pairs))
         self._handle_tickers(out)

   async def start(self) -> None: 
      try:
         if self.exchange is not None:
            await self._watchers()
      except (KeyboardInterrupt, asyncio.CancelledError):
         print("Stopping watchers...")
      except Exception as e:
         print(e)
      finally:
         await self.exchange.close()
         print(f"{self.ex_name} exchange closed.")
