import sys
import os
import yaml
import pydash
from typing import Literal, Dict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config():
   def __init__(self, runs_on: Literal["local", "prod"] | None) -> None:
      if runs_on is None:
         raise Exception("Missing runs_on file")
      
      self._runs_on = runs_on
      self._config: Dict = {}

   def _merge(self, s1: Dict, s2: Dict) -> None:
      self._config = pydash.merge(s1, s2)

   def load(self) -> None:
      default_settings = os.path.join(BASE_DIR, "settings", "default.settings.yml")
      other_settings = os.path.join(BASE_DIR, "settings", f"{self._runs_on}.settings.yml")

      with open(default_settings, "r") as file1:
         setting_1 = yaml.safe_load(file1)

      with open(other_settings, "r") as file2:
         setting_2 = yaml.safe_load(file2)

      self._merge(setting_1, setting_2)

      
   def get_config(self) -> Dict:
      return self._config
   