# coding: utf-8

from slackbot.bot import respond_to
import http.client
from urllib.parse import urlencode, quote_plus
import json
from datetime import tzinfo,timedelta,datetime,timezone
import os

MASTER_DAYS = [
            {"date": "2018-03-01"},
            {"date": "2018-05-29"},
            {"date": "2018-07-27"},
            {"date": "2018-07-28"},
            {"date": "2018-10-24"},
        ]

def get_no_alcohol_day():
    message = ""
    for day in MASTER_DAYS:
        message += "- {0}\n".format(day["date"])
    return message

@respond_to('thailand:no-alcohol-day$')
@respond_to('thailand:no-alcohol-day (.*)')
def no_alcohol_day(message, keyword=None):
    notify_message = "Thailand No Alcohol Days\n" + get_no_alcohol_day()
    message.reply(notify_message)
