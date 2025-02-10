import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Main app styling */
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }

        /* Dashboard cards */
        .metric-container {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            border-left: 5px solid #0031b7;
        }

        /* News cards */
        .news-card {
            background-color: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            margin-bottom: 25px;
            transition: transform 0.2s;
        }

        .news-card:hover {
            transform: translateY(-5px);
        }

        /* Sentiment indicators */
        .sentiment-positive {
            color: #28a745;
            font-weight: 600;
            padding: 5px 10px;
            border-radius: 15px;
            background-color: rgba(40, 167, 69, 0.1);
        }

        .sentiment-negative {
            color: #dc3545;
            font-weight: 600;
            padding: 5px 10px;
            border-radius: 15px;
            background-color: rgba(220, 53, 69, 0.1);
        }

        .sentiment-neutral {
            color: #6c757d;
            font-weight: 600;
            padding: 5px 10px;
            border-radius: 15px;
            background-color: rgba(108, 117, 125, 0.1);
        }

        /* Subscription cards */
        .subscription-card {
            background-color: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
            margin: 15px;
            text-align: center;
            transition: transform 0.3s;
        }

        .subscription-card:hover {
            transform: translateY(-10px);
        }

        .subscription-card h3 {
            color: #0031b7;
            font-size: 24px;
            margin-bottom: 15px;
        }

        .subscription-card h2 {
            font-size: 36px;
            margin: 20px 0;
            color: #333;
        }

        .feature-list {
            list-style-type: none;
            padding: 0;
            margin: 25px 0;
        }

        .feature-list li {
            margin: 15px 0;
            color: #555;
            font-size: 16px;
        }

        .feature-list li:before {
            content: "✓";
            color: #0031b7;
            margin-right: 10px;
        }

        .cta-button {
            background-color: #0031b7;
            color: white;
            padding: 12px 30px;
            border-radius: 25px;
            text-decoration: none;
            display: inline-block;
            margin-top: 20px;
            font-weight: 600;
            transition: background-color 0.3s;
        }

        .cta-button:hover {
            background-color: #002796;
        }

        /* Authentication forms */
        .auth-form {
            background-color: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            margin: 40px auto;
        }

        /* Sidebar styling */
        .sidebar-content {
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 15px;
            margin: 10px;
        }
        </style>
    """, unsafe_allow_html=True)