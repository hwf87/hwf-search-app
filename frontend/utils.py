import requests
import streamlit as st


class Tools:
    def __init__(self) -> None:
        self.path = "./style.css"

    def load_css(self):
        with open(self.path) as f:
            css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


class UiSearch:
    def __init__(self, kanban: str) -> None:
        """ """
        self.kanban = kanban
        self.api_base_url = "http://127.0.0.1:8000"

    def card(
        self,
        uid: str,
        title: str,
        details: str,
        posted: str,
        tags: str,
        link: str,
        images: str,
        highlight: str,
    ) -> None:
        limit, tag_html_str = 5, ""
        for tag in tags[:limit]:
            tag_html_str += f"""<span class="tag">{tag}</span>"""
        
        if images == "":
            images = "https://st.hzcdn.com/fimgs/2a91b52a03b73b7d_2749-w458-h268-b0-p0--.jpg"

        if "youtube.com" in link:
            demo_html_str = f"""<iframe width="100%" src="https://www.youtube.com/embed/{uid}" frameborder="0" allowfullscreen></iframe>"""
        elif "ted.com" in link:
            demo_html_str = f"""<iframe width="100%" src="https://embed.ted.com/talks/lang/en/{uid}" frameborder="0" allowfullscreen></iframe>"""
        elif "houzz.com" in link:
            demo_html_str = f"""<img src={images}>"""
        else:
            demo_html_str = f"""<img src={images}>"""

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

        st.write(html_str, unsafe_allow_html=True)

    def popular_tags(self, tags: list) -> None:
        limit, tag_html_str = 9, ""
        for tag in tags[:limit]:
            tag_html_str += f"""<span class="tag" onclick="tag=Life">{tag}</span>"""

        html_str = f"""
        <div class="card-tags">
            {tag_html_str}
        </div>
        """
        st.write(html_str, unsafe_allow_html=True)

    def search(self) -> None:
        """ """
        st.header("Search")
        search_term = st.text_input("Enter to search")
        sort_by = st.selectbox("Sort by:", ("Relevance", "Date"))
        curr_page = st.selectbox("Pages:", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10))

        if search_term:
            st.session_state.should_search = True

        if st.session_state.should_search:
            if curr_page:
                offset = (curr_page - 1) * 10
                res = requests.get(
                    f"{self.api_base_url}/search/{self.kanban}?query={search_term}&offset={offset}&limit=10"
                ).json()
            items, aggregations, suggestions = (
                res["items"],
                res["aggregations"],
                res["suggestions"],
            )
            tags = [agg["key"] for agg in aggregations]
            # suggests = [sug["text"] for sug in suggestions]
            self.popular_tags(tags)

            if sort_by == "Date":
                items = sorted(items, key=lambda k: k.get('posted', '1991-01-01'), reverse=True)
            for body in items:
                title, uid, details, link, posted, tags, images, highlight = (
                    body["title"],
                    body["uid"],
                    body["details"],
                    body["link"],
                    body["posted"],
                    body["tags"],
                    body["images"],
                    body["highlight"],
                )
                tags = ["none"] if tags == [] else tags
                highlight = "...".join(highlight.get("details", ""))
                self.card(uid, title, details, posted, tags, link, images, highlight)
        else:
            if curr_page:
                offset = (curr_page - 1) * 10
                res = requests.get(
                    f"{self.api_base_url}/kanbans/{self.kanban}/items?orderby=desc&offset={offset}&limit=10"
                ).json()
            if sort_by == "Date":
                res.reverse()
            for body in res:
                title, uid, details, link, posted, tags, images, highlight = (
                    body["title"],
                    body["uid"],
                    body["details"],
                    body["link"],
                    body["posted"],
                    body["tags"],
                    body["images"],
                    body["highlight"],
                )
                tags = ["none"] if tags == [] else tags
                highlight = "...".join(highlight.get("details", ""))
                self.card(uid, title, details, posted, tags, link, images, highlight)

    def recommend(self) -> None:
        """ """
        st.header("Ask a Question")
        input_question = st.text_input("Enter to search")
        if input_question:
            res = requests.get(f"{self.api_base_url}/recommend/by/user_query?q={input_question}&offset=0&limit=30").json()
            for body in res:
                title, uid, details, link, posted, tags, images, highlight = (
                    body["title"],
                    body["uid"],
                    body["details"],
                    body["link"],
                    body["posted"],
                    body["tags"],
                    body["images"],
                    body["highlight"],
                )
                tags = ["none"] if tags == [] else tags
                highlight = "...".join(highlight.get("details", ""))
                self.card(uid, title, details, posted, tags, link, images, highlight)

