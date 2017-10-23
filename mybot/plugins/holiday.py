# coding: utf-8

from slackbot.bot import respond_to
import http.client
from urllib.parse import urlencode, quote_plus
import json
from datetime import tzinfo,timedelta,datetime
import pytz

def get_timezone():
    return pytz.timezone('Asia/Bangkok')

def get_holiday(min_time, max_time):
    api_key = os.getenv('GOOGLE_API_KEY', '')
    calendar_id = 'ja.th#holiday@group.v.calendar.google.com'
    api_url = '/calendar/v3/calendars/' + calendar_id + '/events?key=' + api_key + '&singleEvents=true'

    min_time_str = min_time.isoformat()
    max_time_str = max_time.isoformat()
    payload = {'orderBy': 'startTime', 'maxResults': '10', 'timeMin': min_time_str, 'timeMax': max_time_str}
    query = urlencode(payload, quote_via=quote_plus)
    conn = http.client.HTTPSConnection("www.googleapis.com")
    conn.request("GET", api_url + query)

    response = conn.getresponse()
    body = response.read()
    data = json.loads(body.decode('utf-8'))
    if len(data['items']) > 0:
        return data['items'][0]
    else:
        return None

def notify_with_holiday(message, min_time, max_time):
    holiday = get_holiday(min_time, max_time)
    if holiday is None:
        message.reply('Not found holiday')
    else:
        message.reply(holiday['summary'])

@respond_to('holiday (.*)')
def holiday(message, keyword):
    tz = get_timezone()
    if keyword == 'tomorrow':
        today = datettime.today()
        min_time = datetime(today.year, today.month, today.day, tzinfo=tz) + timedelta(days=1)
        max_time = min_time + timedelta(days=1)
        notify_with_holiday(message, min_time, max_time)
    elif keyword == 'today':
        today = datettime.today()
        min_time = datetime(today.year, today.month, today.day, tzinfo=tz)
        max_time = min_time + timedelta(days=1)
        notify_with_holiday(message, min_time, max_time)
    else:
        message.reply('Usage: holiday tomorrow|today')
