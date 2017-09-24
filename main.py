from aiohttp import web
import logging
import os

from aiohttp.web_exceptions import HTTPNotFound

TOKEN = os.environ["sched.telegram.tg_token"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")


async def handle(request):
    token = request.match_info['token']
    if token != TOKEN:
        logger.warning(f"Received telegram webhook with incorrect token: {token}")
        raise HTTPNotFound()

    data = await request.json()
    logger.info(f"Received telegram webhook: {data}")
    return web.Response(text="OK")


app = web.Application()
app.router.add_route('POST', '/telegram/{token}', handle)

web.run_app(app)
