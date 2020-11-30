import json
from RocketChatBot import RocketChatBot
import logger
import parts_history
import cleaner
import reminder
import report

# constants
SERVER = ''
BOTNAME = ''
BOTPASSWORD = ''
PARTS_ID = ''
PARTS_HISTORY_ID = ''

bot = RocketChatBot(BOTNAME, BOTPASSWORD, SERVER)


def update_chat(message, message_id, new_message):
    bot.api.chat_update(room_id=PARTS_ID, msg_id=message_id, text=new_message)


def get_action_card_message(reference_number):
    cleaner.check_triggers()
    channel_history = parts_history.history()
    messages = json.loads(channel_history)
    for message in messages['messages']:
        msg = message['msg']
        if "Please click the link to view the parts order form for customer" in msg:
            action_card_reference_number = msg.split()[-1]
            if action_card_reference_number == reference_number:
                return message
    return 0


def get_completed_action_card_message(reference_number):
    channel_history = parts_history.history()
    messages = json.loads(channel_history)
    for message in messages['messages']:
        msg = message['msg']
        if "has taken care of this for" in msg:
            action_card_reference_number = msg.split()[-1]
            if action_card_reference_number == reference_number:
                return message
    return 0


def get_user_completed_form_message(reference_number):
    channel_history = parts_history.history()
    messages = json.loads(channel_history)
    for message in messages['messages']:
        msg = message['msg']
        if "GOT IT" in msg:
            completed_action_card_reference_number = msg.split()[-1]
            if completed_action_card_reference_number == reference_number:
                return message
    return


def action_event(msg, user, channel_id):
    message_id = msg['_id']
    ts = msg['ts']
    message = msg['msg']
    content = message.split()
    del content[:3]
    content.pop()
    content = " ".join(content)
    message = message.split()[-1]
    action_card_message = get_action_card_message(message)
    if action_card_message is 0:
        print(user + "tried to take care of " + message + " [already completed]")
        bot.api.chat_post_message(text= user + ", parts order " + message + " is already taken care of.", room_id=PARTS_ID)
        bot.api.chat_delete(room_id=channel_id, msg_id=message_id)
        return
    action_card_id = action_card_message['_id']
    new_message = user + " has taken care of this for " + content + " -- " + message
    print("[" + ts + "]: " + user + " took care of " + message)
    update_chat(action_card_message, action_card_id, new_message)
    parts_history.archive_action_card(message)
    parts_history.archive_user_completed_button(message)


def main():
    print("PartsBot starting")
    bot.add_dm_handler('got it', action_event)
    report.add_report_commands()
    print('Bot DM commands added')
    cleaner.clean_timer()
    print("Cleaning module started")
    reminder.start_reminders()
    print('Reminder module started')
    try:
        bot.run()
        logger.log_info_event("Parts bot started.")
    except:
        print("Timeout occured on main thread")
        logger.log_error_event("Parts bot timed out or errored.")


main()
