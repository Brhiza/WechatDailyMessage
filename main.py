from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = start_date[5:]
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

def get_time():
  dictDate={'Monday':'星期一','Tuesday':'星期二','Wednesday':'星期三','Thursday':'星期四','Friday':'星期五','Saturday':'星期六','Sunday':'星期天'}
  a=dictDate[datetime.now().strftime('%A')]
  return datetime.now().strftime("%Y年%m月%d日 %H时%M分 ")+a

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['hign']), math.floor(weather['low']), weather['city']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    year=next.year + 1
    next = next.replace(year)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, tem_high,tem_low,tem_city = get_weather()

data['weather'] = {'value': wea, 'color': '#002fa4'}
data['city'] = {'value': city, 'color': get_random_color()}
data['tem_high'] = {'value': tem_high, 'color': '#470024'}
data['tem_low'] = {'value': tem_low, 'color': '#01847F'}
data['time'] = {'value': get_time(), 'color': get_random_color()}
data['born_days'] = {'value': get_count(), 'color': get_random_color()}
data['birthday'] = {'value': get_birthday(), 'color': get_random_color()}
data['words'] = {'value': get_words(), 'color': get_random_color()}

res = wm.send_template(user_id, template_id, data)
print(res)
print(get_count())
