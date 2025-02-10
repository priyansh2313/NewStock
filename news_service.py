import requests
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

class NewsService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"

    def get_placeholder_news(self):
        """Return placeholder news while waiting for API key"""
        return pd.DataFrame([
            {
                'title': 'Welcome to Stock News & Analysis',
                'summary': 'Please add your Alpha Vantage API key to see real-time stock news and market updates.',
                'url': 'https://www.alphavantage.co/support/#api-key',
                'time_published': datetime.now(),
                'overall_sentiment_score': 0.0,
                'overall_sentiment_label': 'Neutral'
            }
        ])

    def get_news(self, topics=None, tickers=None):
        @st.cache_data(ttl=900)  # Cache for 15 minutes
        def fetch_news(_api_key, _topics=None, _tickers=None):
            if not _api_key or _api_key == "":
                return self.get_placeholder_news()

            params = {
                "function": "NEWS_SENTIMENT",
                "apikey": _api_key,
                "limit": 50
            }

            if _topics:
                params["topics"] = _topics
            if _tickers:
                params["tickers"] = _tickers

            try:
                response = requests.get(self.base_url, params=params)
                data = response.json()

                if "feed" not in data:
                    if "Note" in data:
                        st.error(f"API Error: {data['Note']}")
                    else:
                        st.error("Unable to fetch news. Please check your API key.")
                    return self.get_placeholder_news()

                news_items = []
                for item in data["feed"]:
                    news_items.append({
                        "title": item["title"],
                        "summary": item["summary"],
                        "url": item["url"],
                        "time_published": datetime.strptime(item["time_published"], "%Y%m%dT%H%M%S"),
                        "overall_sentiment_score": item.get("overall_sentiment_score", 0),
                        "overall_sentiment_label": item.get("overall_sentiment_label", "neutral")
                    })

                return pd.DataFrame(news_items)
            except Exception as e:
                st.error(f"Error fetching news: {str(e)}")
                return self.get_placeholder_news()

        if not self.api_key or self.api_key == "":
            st.warning("⚠️ Alpha Vantage API key is missing. Please add your API key to see real-time news.")
            return self.get_placeholder_news()

        return fetch_news(self.api_key, topics, tickers)

    def display_news(self, df):
        if df.empty:
            st.warning("No news articles available at the moment.")
            return

        for _, row in df.iterrows():
            sentiment_class = row['overall_sentiment_label'].lower()
            time_ago = (datetime.now() - row['time_published']).total_seconds() / 3600

            st.markdown(f"""
            <div class="news-card">
                <h3>{row['title']}</h3>
                <p style="color: #666; margin: 10px 0;">
                    {row['summary'][:200]}...
                </p>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
                    <span style="color: #666;">
                        {row['time_published'].strftime('%Y-%m-%d %H:%M:%S')}
                        ({int(time_ago)} hours ago)
                    </span>
                    <span class="sentiment-{sentiment_class}">
                        {row['overall_sentiment_label']} ({row['overall_sentiment_score']:.2f})
                    </span>
                </div>
                <a href="{row['url']}" target="_blank" style="
                    display: inline-block;
                    margin-top: 10px;
                    color: #0031b7;
                    text-decoration: none;
                    font-weight: 600;
                ">Read more →</a>
            </div>
            """, unsafe_allow_html=True)