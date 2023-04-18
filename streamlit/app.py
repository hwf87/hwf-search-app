import requests
import streamlit as st

with open('./style.css') as f:
    css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

if "should_search" not in st.session_state:
    st.session_state.should_search = False

def card(uid: str, title: str, details: str, posted: str, tags: str, link: str, highlight: str):
    limit, tag_html_str = 5, ""
    for tag in tags[:limit]:
        tag_html_str += f"""<span class="tag">{tag}</span>"""

    if "youtube.com" in link:
        demo_html_str = f"""<iframe width="100%" src="https://www.youtube.com/embed/{uid}" frameborder="0" allowfullscreen></iframe>"""
    elif "ted.com" in link:
        demo_html_str = f"""<iframe width="100%" src="https://embed.ted.com/talks/lang/en/{uid}" frameborder="0" allowfullscreen></iframe>"""
    elif "houzz.com" in link:
        demo_html_str = f"""<img src="https://st.hzcdn.com/fimgs/2a91b52a03b73b7d_2749-w458-h268-b0-p0--.jpg">"""
    else:
        demo_html_str = f"""<img src="https://st.hzcdn.com/fimgs/2a91b52a03b73b7d_2749-w458-h268-b0-p0--.jpg">"""

    # <img src="https://st.hzcdn.com/fimgs/2a91b52a03b73b7d_2749-w458-h268-b0-p0--.jpg">
    # <iframe width="100%" src="https://www.youtube.com/embed/aGXNkUQf56g" frameborder="0" allowfullscreen></iframe>
    html_str = f"""
    <div class="card">
        <div class="card-image">
            {demo_html_str}
        </div>
        <div class="card-content">
            <h5 class="card-title"><a href={link}>{title}</a></h5>
            <p class="card-time">{posted}</p>      
            <p class="card-summary">{(highlight+"..."+details)[:300]}...</p>
            <div class="card-tags">
                {tag_html_str}
            </div>
        </div>
    </div>
    """

    st.write(
        html_str,
        unsafe_allow_html=True
    )

def popular_tags(tags: list):
    limit, tag_html_str = 9, ""
    for tag in tags[:limit]:
        tag_html_str += f"""<span class="tag">{tag}</span>"""

    html_str = f"""
    <div class="card-tags">
        {tag_html_str}
    </div>
    """
    st.write(
        html_str,
        unsafe_allow_html=True
    )

# 定義搜尋和排序功能
def search_and_sort(df, query, sort_by):
    results = df[df['Product'].str.contains(query)]
    results = results.sort_values(by=sort_by, ascending=False)
    return results

# 定義分頁
tabs = ['Main Page', 'Kanban: News', 'Kanban: House', 'Kanban: Talks']
tab = st.sidebar.radio('Select a tab', tabs)

# 如果用戶選擇了搜尋分頁，則顯示搜尋框和結果
if tab == 'Main Page':
    st.header("Product Search")
    search_term = st.text_input("Enter a product name to search")
    if search_term:
        st.session_state.should_search = True

    if st.session_state.should_search:
        res = requests.get(f"http://127.0.0.1:8000/search/hwf_1?query={search_term}&offset=0&limit=20").json()
        items, aggregations, suggestions = res["items"], res["aggregations"], res["suggestions"]
        tags = [agg["key"] for agg in aggregations]
        suggests = [sug["text"] for sug in suggestions]
        popular_tags(tags)

        for body in items:
            title, uid, details, link, posted, tags, highlight = body["title"], body["uid"], body["details"], body["link"], \
                                                                body["posted"], body["tags"], body["highlight"]
            highlight = "...".join(highlight.get("details", ""))
            card(uid, title, details, posted, tags, link, highlight)

        # st.write(res, unsafe_allow_html=True)
    else:
        res = requests.get(f"http://127.0.0.1:8000/kanbans/hwf_1/items?orderby=desc&offset=0&limit=10").json()
        for body in res:
            title, uid, details, link, posted, tags, highlight = body["title"], body["uid"], body["details"], body["link"], \
                                                                body["posted"], body["tags"], body["highlight"]
            highlight = "...".join(highlight.get("details", ""))
            card(uid, title, details, posted, tags, link, highlight)
        # st.write(res, unsafe_allow_html=True)


    # results = search_and_sort(df, query, 'Rating')
    # st.table(results)
    

    # st.write(tmp, unsafe_allow_html=True)

st.session_state.should_search = False