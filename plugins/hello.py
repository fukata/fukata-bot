# coding: utf-8

from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply

@respond_to('hello')
def hello_func(message):
    message.reply('Hello')
