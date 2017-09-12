# coding: utf-8

import os

DEBUG = True
API_TOKEN = os.getenv('SLACK_API_TOKEN', '')
DEFAULT_REPLY = "Sorry, I couldn't understand your message."
PLUGINS = [
#    'slackbot.plugins',
    'mybot.plugins',
]
