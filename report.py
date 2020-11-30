import main
import json
import parts_history
import logger


def report_forms(msg, user, channel_id):
    print(user + " requested open form count")
    message_history = parts_history.history()
    messages = json.loads(message_history)
    count = 0
    for message in messages['messages']:
        if "Please click the link to view the parts order form" in message['msg']:
            count += 1
    count_message = ""
    if count == 1:
        count_message = "There is 1 form that needs to be taken care of."
    else:
        count_message = "There are " + str(count) + " forms that need to be taken care of."

    main.bot.send_message(count_message, channel_id=channel_id)
    logger.log_info_event(user + " requested form count: " + str(count))


def add_report_commands():
    main.bot.add_dm_handler('form count', report_forms)
