import json
import os,sys
import requests
from datetime import datetime
from django.contrib import messages
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.views import View

from django.http import HttpResponseForbidden, HttpResponse

from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FollowEvent, UnfollowEvent,TextSendMessage, ImageMessage, AudioMessage

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError
from django.views.decorators.csrf import csrf_exempt

#channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
#channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
# # if channel_secret is None:
# #     print('Specify LINE_CHANNEL_SECRET as environment variable.')
# #
# #     sys.exit(1)
#
#if channel_access_token is None:
#    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
#    sys.exit(1)
#
#line_bot_api = LineBotApi(channel_access_token)
# # handler = WebhookHandler(channel_secret)



class Hello(View):
    def get(self,request):
        context = {
            'message': "helloWorld",
        }
        times = datetime.now()
        time = {"time": times}
        return render(request, "hello.html", context)


hello = Hello.as_view()

# key = os.getenv('key', None)
key= "b435cd2cb9e26119846645c5f78f9140"

# @handler.add(MessageEvent, message=TextMessage)
class Sample(View):
    def get(self,request):
        weather_data = {}

        BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?id={}&APPID={}"
        url = BASE_URL.format(1853909, key)
        response = requests.get(url).json()
        #jsonText = json.dumps(data, indent=4)
        #jsonText = json.load(jsonText)
        #forecastData = json.loads(jsonText.text)

        for i in response["list"]:
            a={
                "jsonText":i["weather"][0]["id"],
                "date_data" :i["dt_txt"]
            }
            weather_data.update(a)
        # context = {'weather_data': weather_data}
        #
        # profile = line_bot_api.get_profile(event.source.user_id)
        #
        # try:
        #     line_bot_api.push_message(profile, TextSendMessage(text='Hello World!'))
        # except LineBotApiError as e:
        #     print(e)

        return TemplateResponse(request,"app1/sample.html",weather_data)


sample = Sample.as_view()


# @handler.add(MessageEvent, message=TextMessage)
# def handle_push_message():
#     try:
#         line_bot_api.push_message("Uc148172028f01d4635bdb232e6b00920", TextSendMessage(text='Hello World?'))
#     except LineBotApiError as e:
#         return e
#
#         # error handle
#         ...
#
