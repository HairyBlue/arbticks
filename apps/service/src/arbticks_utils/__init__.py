from enum import Enum

name = "arbticks_utils"

supported_pairs = (
      # Extremely High Liquidity
      "BTC/USDT",
      "ETH/USDT",
      # "BTC/USD",
      # "ETH/USD",

      # High Liquidity
      "SOL/USDT",
      # "BNB/USDT",
      # "DOGE/USDT",
      "BTC/USDC",
      "ETH/USDC",
      "ETH/BTC",
      # "SOL/USD",
      # "BNB/USD",
      # "DOGE/USD",
      # "SOL/BTC",
      # "BNB/BTC"
)


__all__ = ["supported_pairs"]