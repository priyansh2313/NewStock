from textblob import TextBlob
import streamlit as st

class SentimentAnalyzer:
    @staticmethod
    def analyze_text(text):
        analysis = TextBlob(text)
        
        # Get polarity score (-1 to 1)
        polarity = analysis.sentiment.polarity
        
        # Determine sentiment label
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
            
        return {
            "score": polarity,
            "label": sentiment
        }

    def display_sentiment_analysis(self, text):
        st.markdown("""
        <style>
        .sentiment-box {
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .positive {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
        }
        .negative {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
        }
        .neutral {
            background-color: #e2e3e5;
            border: 1px solid #d6d8db;
        }
        </style>
        """, unsafe_allow_html=True)

        if text:
            result = self.analyze_text(text)
            
            st.markdown(f"""
            <div class="sentiment-box {result['label']}">
                <h4>Sentiment Analysis Result:</h4>
                <p>Sentiment: {result['label'].title()}</p>
                <p>Score: {result['score']:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
