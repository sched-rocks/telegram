import asyncio
import logging
import os

import telepot
from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound
from telepot.aio import Bot
from telepot.aio.loop import Webhook, MessageLoop

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

TOKEN = os.environ["sched.telegram.tg_token"]


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat Message:', content_type, chat_type, chat_id)


bot = Bot(TOKEN)
webhook = Webhook(bot, {
    'chat': on_chat_message
})

# loop = asyncio.get_event_loop()
# loop.create_task(MessageLoop(bot).run_forever())


async def handle(request):
    token = request.match_info['token']
    if token != TOKEN:
        logger.warning(f"Received telegram webhook with incorrect token: {token}")
        raise HTTPNotFound()

    data = await request.json()
    logger.info(f"Received telegram webhook: {data}")
    webhook.feed(data)
    return web.Response(text="OK")


app = web.Application()
app.router.add_route('POST', '/telegram/{token}', handle)

web.run_app(app)
