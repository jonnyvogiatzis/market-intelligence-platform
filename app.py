import streamlit as st

# Configure the app - this is the first thing Streamlit reads
st.set_page_config(
    page_title="Market Intelligence Platform",
    page_icon="📈",
    layout="wide"  # Uses the full width of the browser
)

# Main page content
st.title("📈 Market Intelligence Platform")
st.markdown("Welcome to your personal market intelligence dashboard.")
st.markdown("Use the sidebar to navigate between pages.")