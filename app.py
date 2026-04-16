import streamlit as st
import pathlib

st.set_page_config(
    page_title="FBJ × Amphora — 3PL Financial Model",
    page_icon="📊",
    layout="wide",
)

# Hide Streamlit chrome so the app feels standalone
st.markdown("""
<style>
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
iframe { border: none; }
</style>
""", unsafe_allow_html=True)

html = pathlib.Path("index.html").read_text(encoding="utf-8")
st.components.v1.html(html, height=1100, scrolling=True)
