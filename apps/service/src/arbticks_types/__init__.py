name = "arbticks_types"

from typing import Literal

# Gikan sa Typescript tawa, pati python gipugus type
ExchangeName = Literal[
   "binance", 
   "kraken",
   "bybit",
   "okx",
   "gate",
   "bitget",
   "mexc",
   "kucoin",
   "htx",
   "bingx"
]

__all__ = ["ExchangeName"]