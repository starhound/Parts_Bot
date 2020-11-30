import logging

logging.basicConfig(filename='partsbot.log', level=logging.INFO)


def log_info_event(log):
    logging.info(log)


def log_error_event(log):
    logging.error(log)


def log_warning_event(log):
    logging.warning(log)

