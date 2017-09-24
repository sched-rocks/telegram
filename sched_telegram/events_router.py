import logging
import os

import telepot
import telepot.loop
from telepot.aio import Bot
from sched_telegram.commands import command_mapping

TOKEN = os.environ["sched.telegram.tg_token"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("events_router")

bot = Bot(TOKEN)


async def handle_update(update):
    # noinspection PyProtectedMember
    event_type, event_data = telepot.loop._extract_message(update)
    if event_type == "message":
        await _handle_message(event_data)
    else:
        logger.warning(f"Received unsupported event type: {event_type}. Data: {event_data}")


async def _handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        await _handle_text_message(msg)
    else:
        logger.warning(f"Received unsupported message type: {content_type}. Data: {msg}")


async def _handle_text_message(msg):
    chat_type = msg["chat"]["type"]
    msg_text = msg["text"]  # type: str

    if msg_text.startswith("/"):
        cmd = msg_text.split(" ")[0]
        command_handler = command_mapping[chat_type][cmd]
        if command_handler:
            await command_handler(msg, bot, {})
        else:
            logger.warning(f"Unknown command: {cmd}")
