__all__ = ("TypeTickerInfo",  "TypeTicker", "TypeTickerMap")
from typing import TypedDict, Optional, Dict, Literal

class TypeTickerInfo(TypedDict, total=False):
    e: str
    E: int
    s: str
    p: str
    P: str
    w: str
    x: str
    c: str
    Q: str
    b: str
    B: str
    a: str
    A: str
    o: str
    h: str
    l: str
    v: str
    q: str
    O: int
    C: int
    F: int
    L: int
    n: int


class TypeTicker(TypedDict):
    symbol: str
    timestamp: int
    datetime: str
    high: float
    low: float
    bid: float
    bidVolume: float
    ask: float
    askVolume: float
    vwap: float
    open: float
    close: float
    last: float
    previousClose: float
    change: float
    percentage: float
    average: float
    baseVolume: float
    quoteVolume: float
    info: TypeTickerInfo
    indexPrice: Optional[float]
    markPrice: Optional[float]


TypeTickerMap = Dict[str, TypeTicker]  # {"ETH/USDC": Ticker, ...}