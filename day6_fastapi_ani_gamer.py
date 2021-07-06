from typing import Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pyquery import PyQuery as pq
from requests_html import HTMLSession


app = FastAPI()
user_dict = {}

@app.get("/test")
def abc():
# check 127.0.0.1:5000/test
    return "In test page"


@app.get("/")
def hello():
# check 127.0.0.1:5000
    return "Hello World!"


@app.get("/ani_gamer")
def ani_gamer_get_list():
    # 獲取請求對象 
    session = HTMLSession() 
    # 往巴哈姆特動畫瘋發送get請求 
    ani_gamer = session.get('https://ani.gamer.com.tw/')
    print(f"ani_gamer.text = {ani_gamer.text}")
    # 利用 Pyquery 文本解析
    page = pq(ani_gamer.text) 
    anime_list = []
    # 萃取出本季的動畫列表並回傳
    for anime_name in page.find(".anime-name_for-marquee"):
        anime_list.append(pq(anime_name).text())
    print(f"anime_list = {anime_list}")
    return " ".join(anime_list)

@app.get("/ani_gamer_json")
def ani_gamer_get_json():
    # 獲取請求對象 
    session = HTMLSession() 
    # 往巴哈姆特動畫瘋發送get請求 
    ani_gamer = session.get('https://ani.gamer.com.tw/')
    print(f"ani_gamer.text = {ani_gamer.text}")
    # 利用 Pyquery 文本解析
    page = pq(ani_gamer.text) 
    anime_dict = {}
    # 萃取出本季的動畫列表並回傳
    for block in page.find(".anime-block"):
        anime_name = pq(block).find(".anime-name_for-marquee").text()
        href =  "https://ani.gamer.com.tw/" + pq(block).find(".anime-card-block").attr("href")
        anime_episode = pq(block).find(".anime-episode").text()
        # print(f"======={anime_name}========")
        # print(f"最新連載 = {anime_episode}")
        # print(f"連結 = {href}")
        # print()
        anime_dict[f"{anime_name}_{anime_episode}"] = href
    print(f"anime_dict = {anime_dict}")
    return anime_dict
#   In fastapi, it will wrap dict to json
#     return jsonify(anime_dict)

@app.get("/ani_gamer_query_weekofday/{dayofweek}")
def ani_gamer_query_weekofday(dayofweek:str):
    week_ = ['Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat', 'Sun']
    assert dayofweek in week_
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
    # print(anime_dict)
    return anime_dict[cht_dayofweek]

        