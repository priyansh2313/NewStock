import streamlit as st
from auth import Authentication
from news_service import NewsService
from sentiment_analyzer import SentimentAnalyzer
from email_service import EmailService
from utils import initialize_session_state, create_sidebar
from styles import apply_custom_styles
import pandas as pd

# Initialize services
auth = Authentication()
news_service = NewsService(st.secrets["ALPHA_VANTAGE_API_KEY"])
sentiment_analyzer = SentimentAnalyzer()
email_service = EmailService("smtp.gmail.com", 587, "your_email@gmail.com", "your_password")

# Apply custom styles
apply_custom_styles()

# Initialize session state
initialize_session_state()

# Create sidebar navigation
page = create_sidebar()

def show_dashboard():
    st.title("📈 Stock Market Dashboard")

    # Display market overview with enhanced styling
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Market Sentiment", "Positive", "+2.5%")
    with col2:
        st.metric("Active Markets", "Global", "24/7")
    with col3:
        st.metric("News Updates", "Real-time", "15min")
    st.markdown('</div>', unsafe_allow_html=True)

    # Market Summary
    st.subheader("📊 Market Summary")
    with st.container():
        summary_col1, summary_col2 = st.columns(2)
        with summary_col1:
            st.markdown("""
            <div class="metric-container">
                <h4>Top Gainers</h4>
                <p>AAPL +3.2%</p>
                <p>GOOGL +2.8%</p>
                <p>MSFT +2.5%</p>
            </div>
            """, unsafe_allow_html=True)
        with summary_col2:
            st.markdown("""
            <div class="metric-container">
                <h4>Market Trends</h4>
                <p>Technology: Bullish</p>
                <p>Healthcare: Neutral</p>
                <p>Energy: Bearish</p>
            </div>
            """, unsafe_allow_html=True)

    # Display recent news
    st.subheader("📰 Recent Market News")
    news_df = news_service.get_news()
    news_service.display_news(news_df)

def show_news():
    st.title("📰 Stock News")

    # Add filters with better styling
    col1, col2 = st.columns(2)
    with col1:
        search = st.text_input("🔍 Search News")
    with col2:
        sentiment_filter = st.selectbox(
            "🎯 Filter by Sentiment",
            ["All", "Positive", "Neutral", "Negative"]
        )

    news_df = news_service.get_news()

    # Apply filters
    if search:
        news_df = news_df[
            news_df['title'].str.contains(search, case=False) |
            news_df['summary'].str.contains(search, case=False)
        ]

    if sentiment_filter != "All":
        news_df = news_df[
            news_df['overall_sentiment_label'].str.lower() == sentiment_filter.lower()
        ]

    news_service.display_news(news_df)

def show_sentiment_analysis():
    st.title("🎯 Sentiment Analysis")

    st.markdown("""
    <div class="metric-container">
        <p>Input any stock-related news or social media text to analyze its sentiment.</p>
    </div>
    """, unsafe_allow_html=True)

    text_input = st.text_area(
        "Enter news or social media text to analyze",
        height=150
    )

    if st.button("🔍 Analyze Sentiment", type="primary"):
        sentiment_analyzer.display_sentiment_analysis(text_input)

def show_subscription():
    st.title("💎 Premium Features")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="subscription-card">
            <h3>Basic Plan</h3>
            <h2>Free</h2>
            <ul class="feature-list">
                <li>Basic news access</li>
                <li>Limited sentiment analysis</li>
                <li>Daily email digest</li>
                <li>Standard support</li>
            </ul>
            <a href="#" class="cta-button">Current Plan</a>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="subscription-card">
            <h3>Premium Plan</h3>
            <h2>$19.99/month</h2>
            <ul class="feature-list">
                <li>Full news access</li>
                <li>Advanced sentiment analysis</li>
                <li>Real-time alerts</li>
                <li>Priority support</li>
                <li>Custom watchlists</li>
                <li>Advanced market insights</li>
            </ul>
            <a href="#" class="cta-button">Upgrade Now</a>
        </div>
        """, unsafe_allow_html=True)

def main():
    if not st.session_state['authenticated']:
        if page == "Login":
            auth.login_form()
        else:  # Register
            auth.register_form()
    else:
        if page == "Dashboard":
            show_dashboard()
        elif page == "News":
            show_news()
        elif page == "Sentiment Analysis":
            show_sentiment_analysis()
        elif page == "Subscription":
            show_subscription()
        elif page == "Settings":
            st.title("⚙️ Settings")
            if st.button("🚪 Logout"):
                auth.logout()
                st.experimental_rerun()

if __name__ == "__main__":
    main()