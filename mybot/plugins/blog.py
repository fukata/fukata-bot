# coding: utf-8

from slackbot.bot import respond_to
import http.client
from urllib.parse import urlencode, quote_plus
import json

@respond_to('blog (.*)')
def blog(message, keyword):
    payload = {'search': keyword}
    query = urlencode(payload, quote_via=quote_plus)
    conn = http.client.HTTPSConnection("blog.fukata.org")
    conn.request("GET", "/wp-json/wp/v2/posts?" + query)
    response = conn.getresponse()
    body = response.read()
    posts = json.loads(body.decode('utf-8'))
    if len(posts) > 0:
        max_num = 5
        num = max_num if len(posts) > max_num else len(posts)
        for i in range(num):
            message.reply(posts[i]['link'])
    else:
        message.reply('Not found posts by keyword=' + keyword)
