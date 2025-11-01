from typing import TypedDict, Dict

class TypeTickerSinkValue(TypedDict): 
   ask: float
   ask_volume: float
   bid: float
   bid_volume: float
   last_update: int

TypeTickerSink = Dict[str, TypeTickerSinkValue]

__all__ = ["TypeTickerSink", "TypeTickerSinkValue"]