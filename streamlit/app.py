import requests
import streamlit as st
import pandas as pd

# 定義假的資料集
data = {
    'Product': ['Product A', 'Product B', 'Product C', 'Product D'],
    'Price': [10, 20, 30, 40],
    'Rating': [3.5, 4.2, 2.7, 4.5],
    'Description': ['Description A', 'Description B', 'Description C', 'Description D']
}

df = pd.DataFrame(data)

if "should_search" not in st.session_state:
    st.session_state.should_search = False

def load_css() -> str:
    """ Return all css styles. """
    common_tag_css = """
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: .15rem .40rem;
                position: relative;
                text-decoration: none;
                font-size: 95%;
                border-radius: 5px;
                margin-right: .5rem;
                margin-top: .4rem;
                margin-bottom: .5rem;
    """
    return f"""
        <style>
            #tags {{
                {common_tag_css}
                color: rgb(88, 88, 88);
                border-width: 0px;
                background-color: rgb(240, 242, 246);
            }}
            #tags:hover {{
                color: black;
                box-shadow: 0px 5px 10px 0px rgba(0,0,0,0.2);
            }}
            #active-tag {{
                {common_tag_css}
                color: rgb(246, 51, 102);
                border-width: 1px;
                border-style: solid;
                border-color: rgb(246, 51, 102);
            }}
            #active-tag:hover {{
                color: black;
                border-color: black;
                background-color: rgb(240, 242, 246);
                box-shadow: 0px 5px 10px 0px rgba(0,0,0,0.2);
            }}
        </style>
    """

url = "http://localhost:8501/#product-search"
title = "Hello"
author = "James"
length = "100"
highlights = "YA Ya Ya"

tmp = f"""
        <div style="font-size:120%;">
            {1 + 1}.
            <a href="{url}">
                {title}
            </a>
        </div>
        <div style="font-size:95%;">
            <div style="color:grey;font-size:95%;">
                {url[:90] + '...' if len(url) > 100 else url}
            </div>
            <div style="float:left;font-style:italic;">
                {author} ·&nbsp;
            </div>
            <div style="color:grey;float:left;">
                {length} ...
            </div>
            {highlights}
        </div>
    """

def youtube_card(title, video_id, text, image, preview_url):
    st.write(
        f"""
        <div style="background-color:#F5F5F5;border-radius:10px;padding:10px;margin:10px">
            <h2>{title}</h2>
            <h4>{video_id}</h4>
            <p>{text}</p>
            <img src="{image}" alt="{title}" style="width:100%;border-radius:10px;">
            <iframe src="{preview_url}" width="100%" height="400"></iframe>
            <iframe width="100%" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>
        </div>
        """,
        unsafe_allow_html=True,
    )

def houzz_card(title, video_id, text, image, preview_url):
    st.write(
        f"""
        <div style="background-color:#F5F5F5;border-radius:10px;padding:10px;margin:10px">
            <h2>{title}</h2>
            <h4>{video_id}</h4>
            <p>{text}</p>
            <iframe width="100%" height="315" src="https://embed.ted.com/talks/lang/en/{video_id}" frameborder="0" allowfullscreen></iframe>
        </div>
        """,
        unsafe_allow_html=True,
    )


# 定義搜尋和排序功能
def search_and_sort(df, query, sort_by):
    results = df[df['Product'].str.contains(query)]
    results = results.sort_values(by=sort_by, ascending=False)
    return results

# 定義應用程序的外觀
st.set_page_config(page_title="Product Search and Sort", page_icon=":mag:", layout="wide")

# 定義分頁
tabs = ['Search', 'Sort']
tab = st.sidebar.radio('Select a tab', tabs)

# 如果用戶選擇了搜尋分頁，則顯示搜尋框和結果
st.write(load_css(), unsafe_allow_html=True)
if tab == 'Search':
    st.header("Product Search")
    search_term = st.text_input("Enter a product name to search")
    if search_term:
        st.session_state.should_search = True

    if st.session_state.should_search:
        res = requests.get(f"http://127.0.0.1:8000/search/hwf?query={search_term}&offset=0&limit=2").json()
        st.write(res, unsafe_allow_html=True)
    else:
        res = requests.get(f"http://127.0.0.1:8000/kanbans/tedtalk_1/items?orderby=desc&offset=0&limit=10").json()
        for body in res:
            # print(i)
            # body = list(i.values())[0]
            title = body["title"]
            subtitle = body["uid"]
            text = body["details"]
            image = body["link"]
            preview_url = "https://www.houzz.com/magazine/houzz-tour-office-building-becomes-a-designers-stylish-home-stsetivw-vs~158661016"
            houzz_card(title, subtitle, text, image, preview_url)
        # st.write(res, unsafe_allow_html=True)


    # results = search_and_sort(df, query, 'Rating')
    # st.table(results)
    

    # st.write(tmp, unsafe_allow_html=True)

# 如果用戶選擇了排序分頁，則顯示排序框和結果
if tab == 'Sort':
    st.header("Product Sort")
    sort_by = st.selectbox("Sort by", ['Price', 'Rating'])
    results = search_and_sort(df, '', sort_by)
    st.table(results)


st.session_state.should_search = False

# res = requests.get("http://127.0.0.1:8000/search/hwf?query=hello%20world&offset=0&limit=2")
# print(res.json())