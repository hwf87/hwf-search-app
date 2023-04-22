import streamlit as st
from utils import UiSearch, Tools

if __name__ == "__main__":
    Tools().load_css()
    if "should_search" not in st.session_state:
        st.session_state.should_search = False
    ui = UiSearch(kanban="houzz")
    ui.recommend()
    st.session_state.should_search = False
