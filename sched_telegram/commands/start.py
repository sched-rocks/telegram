from telepot.aio import Bot

from sched_telegram.commands import telegram_command


@telegram_command("/start", chat_type="private")
async def start_command(msg: dict, bot: Bot, context: dict):
    chat_id = msg["chat"]["id"]
    await bot.sendMessage(chat_id, "Hello world")
