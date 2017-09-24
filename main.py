import logging
import os

from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound
from sched_telegram import events_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

TOKEN = os.environ["sched.telegram.tg_token"]


async def handle(request):
    token = request.match_info['token']
    if token != TOKEN:
        logger.warning(f"Received telegram webhook with incorrect token: {token}")
        raise HTTPNotFound()

    data = await request.json()
    logger.info(f"Received telegram webhook: {data}")
    await events_router.handle_update(data)
    return web.Response(text="OK")


app = web.Application()
app.router.add_route('POST', '/telegram/{token}', handle)

web.run_app(app)
