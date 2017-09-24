command_mapping = {}


def telegram_command(command, chat_type="private"):
    """
    Decorator which registers telegram command handlers
    :param command: The command from which user message should be started to be routed to this handler,including slash
                    e.g. "/start" or "/login"
    :param chat_type: One or more (as list) from "private", "channel", "group", "supergroup"
    """
    if type(chat_type) is str:
        chat_type = [chat_type]

    def decorator(fn):
        for t in chat_type:
            if t not in command_mapping:
                command_mapping[t] = {}
            command_mapping[t][command] = fn
        return fn

    return decorator


from sched_telegram.commands import start
