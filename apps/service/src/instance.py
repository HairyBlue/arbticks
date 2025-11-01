import importlib
import asyncio
import ccxt.pro as ccxt
from typing import Dict, Type
from tracker import ExchangeTracker
from arbticks_types import *

exchange_supported: dict[ExchangeName, Type[ccxt.Exchange]] = {
   "binance": ccxt.binance,
   "kraken": ccxt.kraken,
   "bybit": ccxt.bybit,
   "okx": ccxt.okx,
   "gate": ccxt.gate,
   "bitget": ccxt.bitget,
   "mexc": ccxt.mexc,
   "kucoin": ccxt.kucoin,
   "htx": ccxt.htx,
   "bingx": ccxt.bingx
}

to_register: ExchangeName = [
   "binance", 
   "kraken",
   "bybit",
   "okx",
   "gate",
   "bitget",
   # "mexc", # not support spot market ticker
   "kucoin",
   # "htx", # not supported watch ticker, need fetch
   # "bingx" # not supported watch ticker, need fetch
]


class AppInstance():
   def __init__(self, settings: Dict[str, Dict]) -> None:
      self.__ex_tracker = ExchangeTracker(settings=settings)

   async def register_all_tickers(self): 

      
      background_tasks = set()

      for reg in to_register:
         ccxt_exchage = exchange_supported.get(reg, None)
         if ccxt_exchage is not None:
            mod = importlib.import_module(f"exchange.{reg}")
            create_task = asyncio.create_task(mod.register(self.__ex_tracker, ccxt_exchage))
            background_tasks.add(create_task)
      
      await asyncio.gather(*background_tasks)

   def get_tracker(self):
      return self.__ex_tracker