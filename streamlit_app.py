import streamlit as st

st.set_page_config(page_title="Urban Heat Island Analysis", layout="wide")

st.title("🌍 Urban Heat Island Analysis")
st.markdown("### FortGuard Hackathon 2026")

st.write("""
This application analyzes urban heat inequality using FortGuard's Temperature API.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("The Problem")
    st.write("""
    • 1,500+ Americans die yearly from heat
    • Low-income areas are 5-15°F hotter
    • Less vegetation, more concrete
    """)

with col2:
    st.subheader("The Solution")
    st.write("""
    • Environmental Parameters API
    • Satellite View API  
    • Heat Equity Scoring
    """)

st.markdown("---")
st.info("Live demo of Urban Heat Island Analysis for climate justice")
st.write("[GitHub](https://github.com/humerasadaf59-lab/urban-heat-mapper)")