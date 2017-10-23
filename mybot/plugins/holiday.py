# coding: utf-8

from slackbot.bot import respond_to
import http.client
from urllib.parse import urlencode, quote_plus
import json
from datetime import tzinfo,timedelta,datetime
import pytz
import os

def get_holiday_str(holiday):
    # parse schedule date
    holiday_time = datetime.strptime(holiday['start']['date'], "%Y-%m-%d")
    holiday_str = "%s(%s): %s" % (holiday_time.strftime('%Y-%m-%d'), get_weekday_str(holiday_time), holiday['summary'])
    return holiday_str

def get_weekday_str(dt):
    weekday_strs = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return weekday_strs[dt.weekday()]

def get_timezone():
    return pytz.timezone('Asia/Bangkok')

def get_holiday(min_time, max_time, limit):
    api_key = os.getenv('GOOGLE_API_KEY', '')
    calendar_id = 'ja.th#holiday@group.v.calendar.google.com'
    api_url = '/calendar/v3/calendars/' + quote_plus(calendar_id) + '/events?key=' + quote_plus(api_key) + '&singleEvents=true&'

    min_time_str = min_time.isoformat()
    max_time_str = max_time.isoformat()
    payload = {'orderBy': 'startTime', 'maxResults': limit, 'timeMin': min_time_str, 'timeMax': max_time_str}
    print(payload)
    query = urlencode(payload, quote_via=quote_plus)
    conn = http.client.HTTPSConnection("www.googleapis.com")
    conn.request("GET", api_url + query)
    response = conn.getresponse()
    if response.status == 200:
        body = response.read()
        data = json.loads(body.decode('utf-8'))
        item_num = len(data['items'])
        if item_num > 0:
            num = limit if item_num > limit else item_num
            return data['items'][0:num]
        else:
            return None
    else:
        return None

def notify_with_holiday(message, min_time, max_time, limit=1):
    holidays = get_holiday(min_time, max_time, limit)
    if holidays is None:
        message.reply('Not found holiday')
    else:
        notify_message = "Found Holiday. %s - %s" % (min_time.strftime('%Y-%m-%d'), max_time.strftime('%Y-%m-%d'))
        for holiday in holidays:
            notify_message += "\n"
            notify_message += get_holiday_str(holiday)
        message.reply(notify_message)

@respond_to('holiday (.*)')
def holiday(message, keyword):
    tz = get_timezone()
    if keyword == 'tomorrow':
        today = datetime.today()
        min_time = datetime(today.year, today.month, today.day, tzinfo=tz) + timedelta(days=1)
        max_time = min_time + timedelta(days=1)
        notify_with_holiday(message, min_time, max_time)
    elif keyword == 'today':
        today = datetime.today()
        min_time = datetime(today.year, today.month, today.day, tzinfo=tz)
        max_time = min_time + timedelta(days=1)
        notify_with_holiday(message, min_time, max_time)
    else:
        message.reply('Usage: holiday tomorrow|today')

@respond_to('holiday')
def default_holiday(message):
    tz = get_timezone()
    today = datetime.today()
    min_time = datetime(today.year, today.month, today.day, tzinfo=tz)
    max_time = min_time + timedelta(days=90)
    notify_with_holiday(message, min_time, max_time, limit=7)
