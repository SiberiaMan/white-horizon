"""
Микросервис управления проектами разметки
"""

import asyncio
import logging
import typing

from aiohttp import web

from .api import HealthCheckApi
from .config import get_settings

import asyncpg

# from .repositories import (

# )



SERVICE_NAME = "white-horizon-mono"


async def init_pg(app, config):
    conn = await asyncpg.connect(user=config["pg_user"], password=config["pg_pwd"],
                                    database=config["pg_db"], host=config["pg_host"], port=config["pg_port"], timeout=10)
    # try fetch data
    values = await conn.fetch(
        'SELECT * from public.areas',
    )
    print(values)

    app["postgres_db"] = conn



async def on_startup(app):
    logging.debug("Startup")
    # Инициализируем сервисы и клиенты

    await init_pg(app, app["config"])

    HealthCheckApi(app=app)


async def on_shutdown(app):
    app["postgres_db"].close()


def init_app(config: typing.Mapping) -> web.Application:
    app = web.Application(client_max_size=5 * (1024**2))

    app["config"] = config

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    return app


def create_app() -> web.Application:
    settings = get_settings()
    return init_app(settings)
