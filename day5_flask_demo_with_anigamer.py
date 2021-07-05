from flask import Flask, jsonify
from pyquery import PyQuery as pq
from requests_html import HTMLSession


app = Flask(__name__)

@app.route("/test")
def abc():
# check 127.0.0.1:5000/test
    return "In test page"


@app.route("/")
def hello():
# check 127.0.0.1:5000
    return "Hello World!"

@app.route("/ani_gamer")
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

@app.route("/ani_gamer_json")
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
    # return anime_dict
    return jsonify(anime_dict)
    

if __name__ == "__main__":
    # app.run()
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)