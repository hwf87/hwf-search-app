import streamlit as st
from utils import search

if __name__ == "__main__":
    with open('./style.css') as f:
        css = f.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    if "should_search" not in st.session_state:
        st.session_state.should_search = False
    search(kanban = "hwf_1")
    st.session_state.should_search = False