from datetime import date, datetime,, timedelta
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random


nowtime = datetime.utcnow() + timedelta(hours=8)  # 东八区时间
today = datetime.strptime(str(nowtime.date()), "%Y-%m-%d") #今天的日期

start_date ='2020-12-13'
city = '北京'
birthday = '12-17'

app_id = "wx3d3287c20f6f470a"
app_secret = "0939e4b6ca248c4e0d28f36679ca379a"

user_id = "o_TZC5wJ6RfAKFT5TpXD0cYNnVu8"
template_id = "ZYLYUTIJfnWcnuwP0Tgyn8yXoUpL5BW6latlyOTmnbI"


# 获取当前日期为星期几
def get_week_day():
  week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
  week_day = week_list[datetime.date(today).weekday()]
  return week_day

#获取天气
def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

#纪念日
def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

#生日倒计时
def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

#彩虹屁
def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

#获取午餐
def get_lunch():
  menu_meat=['麻辣香锅','咖喱鸡和','青椒鸡丁和','红烧牛肉和', '溜肉段和', '辣子鸡和', '鸡排和' ]
  menu_veg=['青菜' ,'西兰花' ,'番茄炒蛋','素鸡']
  meat=random.choice(menu_meat) 
  veg=random.choice(menu_veg)
  if meat=='麻辣香锅':
    lunch=['麻辣香锅']
  else:
    lunch=meat+veg   
  return lunch


# 随机颜色
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {
  "city": {
    "value": city,
    "color": get_random_color()
  },
  "date": {
    "value": today.strftime('%Y年%m月%d日'),
    "color": get_random_color()
  },
  "week_day": {
    "value": get_week_day(),
    "color": get_random_color()
  },
  "weather": {
    "value": weather['weather'],
    "color": get_random_color()
  },
  "humidity": {
    "value": weather['humidity'],
    "color": get_random_color()
  },

  "air_quality": {
    "value": weather['airQuality'],
    "color": get_random_color()
  },
  "temperature": {
    "value": math.floor(weather['temp']),
    "color": get_random_color()
  },
  "highest": {
    "value": math.floor(weather['high']),
    "color": get_random_color()
  },
  "lowest": {
    "value": math.floor(weather['low']),
    "color": get_random_color()
  },
  
  "love_days":{
    "value":get_count(),
    "color":get_random_color()
  },

  "birthday_left": {
    "value": get_birthday_left(),
    "color": get_random_color()
  },
  
    "lunch": {
    "value": get_lunch(),
    "color": get_random_color()
  },
  
  "words": {
    "value": get_words(),
    "color": get_random_color()
  },
}

res = wm.send_template(user_id, template_id, data)
print(res)
