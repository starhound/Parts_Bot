import main
import parts_history
import json
import datetime
import threading
import logger

PARTS_CHAT = 1


def report_action_card(message):
    message = message["msg"]
    content = message.split(':')
    reminder = "Parts order for " + content + " has been unclaimed for three or more days!"
    main.bot.api.chat_post_message(text=reminder, channel=PARTS_CHAT)
    logger.log_info_event(reminder)


def check_messages():
    message_history = parts_history.history()
    messages = json.loads(message_history)
    dt = datetime.datetime.today()
    date = dt.day
    for message in messages['messages']:
        time = message["ts"]
        message_date = time.split('-')[2]
        if message_date < int(date) - 3:
            report_action_card(message)


def start_reminders():
    threading.Timer(86400.0, check_messages).start()
