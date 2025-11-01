import logging
import json
import os
import datetime
from logging.handlers import RotatingFileHandler
import shutil


base_filename = "svc.log"
folder_path = "logs"

os.makedirs(folder_path, exist_ok=True)

# try:
#     if os.path.exists(folder_path):
#         shutil.rmtree(folder_path)
# except PermissionError as e:
#     print(f"Could not remove {folder_path}: {e}")


class JsonFormatter(logging.Formatter):
   def __init__(self, extra_fields=None, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.extra_fields = extra_fields if extra_fields else []

   def format(self, record):

      log_record = {
         # "timestamp": self.formatTime(record, self.datefmt),
         "level": record.levelname,
         "message": record.getMessage(),
         # "module": record.module,
         # "function": record.funcName,
         # "line": record.lineno,
         # "name": record.name,
      }

      for field in self.extra_fields:
         log_record[field] = getattr(record, field, None)

      return json.dumps(log_record)

class DateRotatingFileHandler(RotatingFileHandler):
    def doRollover(self):
        if self.stream:
            self.stream.close()

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # log_dir, base_filename = os.path.split(self.baseFilename)
        
        new_log_file = f"log-{current_time}.log"
        new_log_file_path = os.path.join(os.path.dirname(self.baseFilename), new_log_file)

        if os.path.exists(new_log_file_path):
            os.remove(new_log_file_path)
        
        os.rename(self.baseFilename, new_log_file_path)

        self.mode = "a"
        self.stream = self._open()



def setup_logger(extra_fields=None):
    log_file = os.path.join(folder_path, base_filename)

    logger = logging.getLogger("JsonLogger")
    logger.setLevel(logging.INFO)
   
    if not logger.handlers:
        handler = DateRotatingFileHandler(
            log_file, maxBytes=50 * 1024, backupCount=0
        )

        json_formatter = JsonFormatter(extra_fields=extra_fields)
        handler.setFormatter(json_formatter)  # Formatter set here
        logger.addHandler(handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(json_formatter)
        logger.addHandler(console_handler)

    return logger


BASE_LOGGER = setup_logger()

def get_logger(name: str):
    base_logger = BASE_LOGGER

    class LoggerWrapper:
        def __init__(self, logger, name):
            self._logger = logger
            self._name = name

        def info(self, *args, **kwargs):
            self._log("INFO", *args, **kwargs)

        def error(self, *args, **kwargs):
            self._log("ERROR", *args, **kwargs)

        def debug(self, *args, **kwargs):
            self._log("DEBUG", *args, **kwargs)

        def _log(self, level, *args, **kwargs):
            # Combine *args into a string or JSON
            combined_message = " ".join([json.dumps(arg) if isinstance(arg, (dict, list)) else str(arg) for arg in args])
            # Merge kwargs if any
            if kwargs:
                combined_message += " " + json.dumps(kwargs)
            log_record = {
                "name": self._name,
                "level": level,
                "message": combined_message
            }
            getattr(self._logger, level.lower())(json.dumps(log_record))

    return LoggerWrapper(base_logger, name)


# --- Logger Wrapper ---
# def get_logger(name: str):
#     base_logger = BASE_LOGGER

#     class LoggerWrapper:
#         def __init__(self, logger, name):
#             self._logger = logger
#             self._name = name

#         def info(self, *args, **kwargs):
#             self._log("INFO", *args, **kwargs)

#         def error(self, *args, **kwargs):
#             self._log("ERROR", *args, **kwargs)

#         def debug(self, *args, **kwargs):
#             self._log("DEBUG", *args, **kwargs)

#         def _log(self, level, *args, **kwargs):
#             # Combine *args into JSON-friendly string
#             combined_message = " ".join(
#                 [json.dumps(arg) if isinstance(arg, (dict, list)) else str(arg) for arg in args]
#             )
#             # Merge kwargs if any
#             extra_data = kwargs if kwargs else None

#             log_record = {
#                 "name": self._name,
#                 "level": level,
#                 "message": combined_message
#             }
#             if extra_data:
#                 log_record["extra_data"] = extra_data

#             getattr(self._logger, level.lower())(json.dumps(log_record))

#     return LoggerWrapper(base_logger, name)

__all__ = ["get_logger"]