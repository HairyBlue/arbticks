import sys
import os
import ccxt.pro as ccxt
import asyncio

from arbticks_utils import supported_pairs
# need to use utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

location = "kraken"