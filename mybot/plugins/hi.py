# coding: utf-8

from slackbot.bot import respond_to
import re

@respond_to('hi', re.IGNORECASE)
def hi_reply(message):
    message.reply('I can understand hi or HI!')
    message.react('+1')
