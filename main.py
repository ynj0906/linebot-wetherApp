import sys,os
from django.core.management import BaseCommand
from linebot.models import MessageEvent, TextMessage, FollowEvent, UnfollowEvent,TextSendMessage, ImageMessage, AudioMessage
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError

if LINE_CHANNEL_ACCESS_TOKEN is None:
    print(1)
    sys.exit(1)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

try:
    line_bot_api.push_message("Uc148172028f01d4635bdb232e6b00920", TextSendMessage(text='Hello World?'))
except LineBotApiError as e:
    print(e)
print("カスタムコマンドを実行")
