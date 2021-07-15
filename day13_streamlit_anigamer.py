import time

from pyquery import PyQuery as pq
from requests_html import HTMLSession
import requests
import pandas as pd
import streamlit as st
from PIL import Image

@st.cache(allow_output_mutation=True)
def ani_gamer_query():
    # 獲取請求對象 
    session = HTMLSession() 
    # 往巴哈姆特動畫瘋發送get請求 
    ani_gamer = session.get('https://ani.gamer.com.tw/') 

    page = pq(ani_gamer.text) 
    df_list = []
    for block in page.find(".anime-block"):
        anime_name = pq(block).find(".anime-name_for-marquee").text()
        anime_episode = pq(block).find(".anime-episode").text()
        href =  "https://ani.gamer.com.tw/" + pq(block).find(".anime-card-block").attr("href")
        img_link =  pq(block).find(".anime-blocker").find("img").attr("src")
        print(f"======={anime_name}========")
        print(f"最新連載 = {anime_episode}")
        print(f"連結 = {href}")
        print(f"img_link = {img_link}")
        df_list += [[anime_name, anime_episode, href, img_link]]
    df = pd.DataFrame(columns=["name", "eposide", "link", "image_link"], data=df_list)
    return df

def run():

    # ===============================
    # Get Anime dataframe
    # ===============================
    anime_df = ani_gamer_query()
    # ===============================
    # Construct demo site by streamlit
    # ===============================
    with st.sidebar:
        st.header("Ani gamer")
        with st.form(key="grid_reset"):
            n_cols = st.slider("Number of columns:", 2, 4, 2)
            st.form_submit_button(label="Get the anime list")
    
    # Create demo columns on website
#      # Load demo images
#     image1 = Image.open('YOUR IMAGE')
#     image2 = Image.open('YOUR IMAGE')
#     demo_left_column, demo_right_column = st.beta_columns(2)
#     demo_left_column.image(image1,  caption = "Demo 1 image")
#     demo_right_column.image(image2, caption = "Demo 2 image")

    
    st.title('Anime gamer - xiaosean')
    st.write(" ------ ")
    
    # Create dataframe by streamlit magic commands
#     anime_df
    st.dataframe(anime_df)  # Same as st.write(df)
    
    # Create grid
    n_anime = len(anime_df)
    n_rows = 1 + n_anime // n_cols
    rows = [st.beta_container() for _ in range(n_rows)]
    cols_per_row = [r.beta_columns(n_cols) for r in rows]

    start_time = time.time()
    for idx in range(n_anime):
        with rows[idx // n_cols]:
            # Generate with alpha and latent code attributes.
#             cols_per_row[image_index // n_cols][image_index % n_cols].image(result)
            name, eposide, link, image_link = anime_df.iloc[idx]
            # im = Image.open(requests.get(image_link, stream=True).raw)
            # cols_per_row[idx // n_cols][idx % n_cols].image(im, caption=f"{name}_{eposide}")
            cols_per_row[idx // n_cols][idx % n_cols].image(image_link, caption=f"{name}_{eposide}")
            cols_per_row[idx // n_cols][idx % n_cols].markdown(f"Go to the [Link!]({link})", unsafe_allow_html=True)
    spend_time = time.time() - start_time
    print(f"Total cost time = {spend_time}")

    
    
if __name__ == '__main__':
    run()