import asyncio
from typing import Callable, Type, Dict
from arbticks_utils import *
from arbticks_types import *
from arbticks_types.type_sink import *
from arbticks_types.type_tickers import *
from tracker import ExchangeTracker
from sink import SinkTicker

class ExchangeManager():
   def __init__(self, ex_name: ExchangeName, ccxt: Callable, ccxt_config: Dict, ex_tracker: Type[ExchangeTracker]) -> None:
      self._enable_watcher = True
      self.__ccxt_exchange = ccxt(ccxt_config)
      self.__ex_name = ex_name
      self.__ex_tracker = ex_tracker

      
   def _handle_tickers(self, ticker_map: TypeTickerMap) -> None:
      sink_ticker = SinkTicker()
      for symbol, value in ticker_map.items():
         ask = value["ask"]
         ask_volume = value["askVolume"]
         bid = value["bid"]
         bid_volume = value["bidVolume"]

         sink_ticker.sink(symbol, ask, ask_volume, bid, bid_volume)
         self.__ex_tracker.update_tracker(self.__ex_name, sink_ticker.get_ticker_sink(), False)   

   async def _watchers(self) -> None:
      while self._enable_watcher:
         try:
            out = await self.__ccxt_exchange.watch_tickers(list(supported_pairs))
            self._handle_tickers(out)
         except Exception as e:
            await asyncio.sleep(10)

   async def start(self) -> None: 
      try:
         if self.__ccxt_exchange is not None:
            await self._watchers()
      except (KeyboardInterrupt, asyncio.CancelledError):
         print("Stopping watchers...")
      except Exception as e:
         print(e)
      finally:
         await self.__ccxt_exchange.close()
         print(f"{self.__ex_name} exchange closed.")
