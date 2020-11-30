import threading
import main
from parts_history import history
import json


def delete_trigger(message):
    msg_id = message["_id"]
    main.bot.api.chat_delete(room_id=main.PARTS_ID, msg_id=msg_id)


def check_triggers():
    channel_history = history()
    messages = json.loads(channel_history)
    for message in messages['messages']:
        msg = message['msg']
        if "!parts" in msg:
            delete_trigger(message)


def clean_channel():
    check_triggers()


def clean_timer():
    check_triggers()
    threading.Timer(180.0, clean_timer).start()
