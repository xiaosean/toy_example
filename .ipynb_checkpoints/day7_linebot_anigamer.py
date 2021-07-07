from datetime import date

from pyquery import PyQuery as pq
from requests_html import HTMLSession
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    commands = ["Hello", "Anime"]
    if event.message.text not in commands:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="機器人並不支援該指令"))
    
    if event.message.text == "Hello":
        reply_text = hello()    
    elif event.message.text == "Anime":
        reply_text = str(ani_gamer_query_today())

#     回傳文字
    print(f"reply_text = {reply_text}")
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text))

def hello():
    return "Hello World!"

def ani_gamer_query_today():
    week_ = ['Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat', 'Sun']
    today = date.today()
    # 獲得今天是禮拜幾
    dayofweek = week_[today.weekday()]
    # 轉換成中文 [Optional]
    cht_week_mapping = {
        "Mon":"週一",
        "Tue":"週二",
        "Wed":"週三",
        "Thr":"週四",
        "Fri":"週五",
        "Sat":"週六",
        "Sun":"週日"
    }
    cht_dayofweek = cht_week_mapping[dayofweek]
    # 獲取請求對象 
    session = HTMLSession() 
    # 往巴哈姆特動畫瘋發送get請求 
    ani_gamer = session.get('https://ani.gamer.com.tw/')
    # 利用 Pyquery 文本解析
    page = pq(ani_gamer.text) 
    anime_dict = {}
    # 萃取出本季的動畫列表並回傳
    for block in page.find(".day-list"):
        day_of_week = pq(block).find(".day-title").text()
        print(f"day_of_week = {day_of_week}")
    #     Create dictionary of day of week
    #   {
    #     週一： {}
    #     週二： {}
    #     週三： {}
    #     ......
    #     週日： {}
    #     }
        anime_dict[f"{day_of_week}"] = {}
        for anime in page(block).find(".text-anime-info"):
            anime_name = pq(anime).find(".text-anime-name").text()
            href =  "https://ani.gamer.com.tw/" + pq(anime).attr("href")
            anime_episode = pq(anime).find(".text-anime-number").text()
            # print(f"======={anime_name}========")
            # print(f"最新連載 = {anime_episode}")
            # print(f"連結 = {href}")
            anime_dict[f"{day_of_week}"][f"{anime_name}_{anime_episode}"] = href
    print(anime_dict)
    return anime_dict[cht_dayofweek]

        


if __name__ == "__main__":
    app.run()