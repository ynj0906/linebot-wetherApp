import sys,os,requests,re
from django.core.management import BaseCommand
from linebot.models import MessageEvent, TextMessage, FollowEvent, UnfollowEvent,TextSendMessage, ImageMessage, AudioMessage
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError
from datetime import date
import datetime
import pathlib
from socket import gethostname
from os import environ
HOSTNAME = gethostname()

if 'DESKTOP' in HOSTNAME:
    # C:\Users\USER\PycharmProjects\linebot_weather\WeatherApp\config\local_settings.py
    # C:\Users\USER\PycharmProjects\linebot_weather\WeatherApp\app1\management\commands\push_mes.py
    # WeatherApp / config / local_settings.py
    # WeatherApp / app1 / management / commands / push_mes.py
    # from ... import config.local_settings
    current_dir = pathlib.Path(__file__).resolve().parent
    sys.path.append(str(current_dir) + '/..../')
    from config import local_settings
    LINE_CHANNEL_ACCESS_TOKEN = local_settings.LINE_CHANNEL_ACCESS_TOKEN
    weather_key = local_settings.weather_key
else:
    channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
    weather_key = os.getenv('key', None)

# if LINE_CHANNEL_ACCESS_TOKEN is None:
#     print(1)
#     sys.exit(1)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

class Command(BaseCommand):
    help = 'ここにコマンドの説明を書けます。'

    # ここに実行したいコマンドを記述
    def handle(self, *args, **options):
        BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?id={}&APPID={}"
        url = BASE_URL.format(1853909, weather_key)
        response = requests.get(url).json()
        # jsonText = json.dumps(data, indent=4)
        # jsonText = json.load(jsonText)
        # forecastData = json.loads(jsonText.text)

        ymd_list=[]
        weathercode_list=[]

        ymd_list.clear()
        weathercode_list.clear()
        g = date.today()
        #天気情報とt天気時間をそれぞれのリストに追加
        for i in response["list"]:
            weathercode_list.append(i["weather"][0]["id"])
            ymd_list.append(i["dt_txt"])
        #それぞれのリストからペアにして辞書型に追加
        # d = {k: {"天気情報": v1, "天気時間": v2} for k , v1, v2 in zip(ymd_list, weathercode_list, ymd_list)}
        final_list=[]
        final_list.clear()
        flag=0

        for k , v1, v2 in zip(ymd_list, weathercode_list, ymd_list):
            k = datetime.datetime.strptime(k, '%Y-%m-%d %H:%M:%S')
            k=k.date()
            day = datetime.datetime.strptime(v2, '%Y-%m-%d %H:%M:%S')
            d = {k: {"天気情報": v1, "天気時間": v2}}
            if day.date() == g:
                if re.match(r"5\d\d", str(d[k]["天気情報"])):
                    d[k]["天気情報"]="雨"
                    flag+=1
                    final_list.append(d)
                elif re.match(r"8\d\d", str(d[k]["天気情報"])):
                    d[k]["天気情報"] = "晴れ"
                    final_list.append(d)
        # if day.date() == g and re.match(r"8\d\d", str(final_list[0][day]["天気情報"])):
        print(final_list)
        print(flag)
        if flag >= 1:
            try:
                line_bot_api.push_message("Uc148172028f01d4635bdb232e6b00920",
                                          [TextSendMessage(text="今日は雨やで！\uDBC0\uDCAA"),
                                           TextSendMessage(text="{}は{}です\n"
                                                                "{}は{}です\n"
                                                                "{}は{}です\n"
                                                                "{}は{}です\n"
                                                                "{}は{}です"
                                                           .format(final_list[0][datetime.date.today()]["天気時間"][10:],
                                                                   final_list[0][datetime.date.today()]["天気情報"],
                                                                   final_list[1][datetime.date.today()]["天気時間"][10:],
                                                                   final_list[1][datetime.date.today()]["天気情報"],
                                                                   final_list[2][datetime.date.today()]["天気時間"][10:],
                                                                   final_list[2][datetime.date.today()]["天気情報"],
                                                                   final_list[3][datetime.date.today()]["天気時間"][10:],
                                                                   final_list[3][datetime.date.today()]["天気情報"],
                                                                   final_list[4][datetime.date.today()]["天気時間"][10:],
                                                                   final_list[4][datetime.date.today()]["天気情報"]
                                                                   ))])
            except LineBotApiError as e:
                return e
        else:
            pass
            # line_bot_api.push_message("Uc148172028f01d4635bdb232e6b00920",
            #                       TextSendMessage(text="いってらっしゃい{}\n{}".format(d[i]["天気時間"],d[i]["天気情報"])))
