import os
import asyncio
from quart import Quart
from quart_schema import QuartSchema, validate_request, validate_response

from flask import Flask
from config import Config
from instance import AppInstance
from routes import *

app = Quart(__name__)
QuartSchema(app)

runs_on = os.getenv('RUNS_ON', 'local')

config = Config(runs_on).load()
config_settings = config.get_config()

app_instance = AppInstance(config_settings)

ex_tracker = app_instance.get_tracker()

@app.before_serving
async def startup():
   asyncio.create_task(app_instance.register_all_tickers())

public_api = create_public_routes(ex_tracker=ex_tracker)
app.register_blueprint(public_api)

if __name__ == "__main__":
   app.run()
