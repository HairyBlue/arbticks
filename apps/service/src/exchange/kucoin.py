import sys
import os
from typing import Type, Callable
from exchange_manager import ExchangeManager
from tracker import ExchangeTracker
# need to use utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

exhange_name = "kucoin"
ccxt_config = {}

async def register(ex_tracker: Type[ExchangeTracker], ccxt_exchage: Callable):
   ex_man = ExchangeManager(ex_name=exhange_name, ccxt=ccxt_exchage, ccxt_config=ccxt_config, ex_tracker=ex_tracker)
   await ex_man.start()

__all__ = ("register")