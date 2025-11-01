from typing import Dict
from arbticks_types.type_sink import *
from arbticks_utils.a_date import *

class ExchangeTracker():
   def __init__(self, settings: Dict[str, Dict]) -> None:
      self.__cache: Dict[str, TypeTickerSink] = {}
      self.__exchange_age: Dict[str, int] = {}
      self.__settings = settings

   def update_tracker(self, exchange: str, tickerSink: TypeTickerSink, merge: bool) -> None:
      if self.__cache.get(exchange) is None:
         self.__cache[exchange] = {}
         self.__exchange_age[exchange] = 1

      for symbol, value in tickerSink.items():
         self.__cache[exchange][symbol] = value

      self.__exchange_age[exchange] = date_now()
   
   def get_cache(self):
      return self.__cache
