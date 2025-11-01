from datetime import datetime, timezone

def date_now() -> int:
   return int(datetime.now(tz=timezone.utc).timestamp() * 1000)


__all__ = ["date_now"]