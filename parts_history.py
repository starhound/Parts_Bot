import main
import logger


def history():
    return main.bot.api.groups_history(room_id=main.PARTS_ID, count=1000).content


def archive_action_card(reference_number):
    completed_form = main.get_completed_action_card_message(reference_number)
    if completed_form is 0:
        return
    link = completed_form['attachments'][0]['text']
    ts = completed_form['ts']
    msg_id = completed_form["_id"]
    message = completed_form['msg']
    user = completed_form['u']['username']
    main.bot.send_message("[" + ts + "]: " + message + " (" + link + ")", channel_id=main.PARTS_HISTORY_ID)
    main.bot.api.chat_delete(room_id=main.PARTS_ID, msg_id=msg_id)
    logger.log_info_event(message + " -- " + link)


def archive_user_completed_button(reference_number):
    card = main.get_user_completed_form_message(reference_number)
    if card is 0:
        return
    msg_id = card["_id"]
    main.bot.api.chat_delete(room_id=main.PARTS_ID, msg_id=msg_id)

