from telebot import TeleBot
from telebot.types import Message
from os import getenv
from sys import exit

import functools
import logging

# configure logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# get variable values from environment variables
allowed_ids = getenv('ALLOWED_USER_IDS', '').split(',')
if allowed_ids[0] == '':
    logger.error(
        'set ALLOWED_USER_IDS in environment variable or .env file')
    exit(-1)
    
allowed_ids = [int(id) for id in allowed_ids]


TELE_BOT_TOKEN = getenv('TELE_BOT_TOKEN', None)
if not TELE_BOT_TOKEN:
    raise ValueError(
        'TELE_BOT_TOKEN should be set in environment variable or stored in .env file')


# create bot
tlbot = TeleBot(
    TELE_BOT_TOKEN,
    parse_mode=None
)


def is_valid_user(func):
    '''
    Decorator function used to whether user has access to the bot or not
    '''
    @functools.wraps(func)
    def decorator(message: Message = None, *args, **kwargs):
        # check if user is valid
        # if user is valid then call func
        # and return its value else it
        # returns False
        if message.from_user.id in allowed_ids:
            return func(message, *args, **kwargs)

        logging.warning(f'Unauthorized user with id {message.from_user.id} and username {message.from_user.username} tried to access the bot. Message sent by the user: {message.text}')
        tlbot.send_message(message.from_user.id, text='Not Authorized')

    return decorator

@tlbot.message_handler(commands=['start'])
def get_user_details(message: Message):
    '''
    replies /start message with messenger's details back to the user
    '''
    tlbot.reply_to(
        message, f'USER ID : {message.from_user.id}\nName : {message.from_user.full_name}\nUserName : {message.from_user.username}\nIs BOT : {message.from_user.is_bot}\nHas Access : {True if message.from_user.id in allowed_ids else False}')


@tlbot.message_handler(commands=['help'])
@is_valid_user
def send_help_message(message):
    '''
    replies back to the user with help message
    '''
    help_message = 'This is help section'
    tlbot.reply_to(message=message, text=help_message)

def send_notification_to_allowed_ids(message:str):
    for user_id in allowed_ids:
        tlbot.send_message(chat_id=user_id, text=message)

# set webhook to notify user
# tlbot.set_webhook()