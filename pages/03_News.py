# 03_News.py
# This page displays financial news articles.
# Users can search for news about any stock or topic.

import streamlit as st
from services.news_service import get_news

st.set_page_config(page_title="News", page_icon="📰", layout="wide")

st.title("📰 Financial News")
st.markdown("Latest financial news from across the web.")

# Search input
query = st.text_input("Search for news:", placeholder="e.g. Apple, Tesla, inflation, Fed rate").strip()

# Use default query if nothing is typed
if not query:
    query = "stock market"

# Fetch news
with st.spinner(f"Loading news for '{query}'..."):
    articles = get_news(query, num_articles=10)

# Display articles
if articles and "error" not in articles[0]:
    for article in articles:
        with st.container():
            st.markdown(f"### [{article['title']}]({article['url']})")
            st.markdown(f"*{article['source']}* — {article['published_at'][:10]}")
            if article['description']:
                st.write(article['description'])
            st.divider()
else:
    st.error("Could not load news. Check your API key.")