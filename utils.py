import streamlit as st

def initialize_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None
    if 'user_email' not in st.session_state:
        st.session_state['user_email'] = None

def create_sidebar():
    with st.sidebar:
        st.image("https://www.svgrepo.com/show/530443/stock.svg", width=100)
        st.title("Stock News & Analysis")
        
        if st.session_state['authenticated']:
            st.write(f"Welcome, {st.session_state['user_email']}")
            return st.sidebar.radio(
                "Navigation",
                ["Dashboard", "News", "Sentiment Analysis", "Subscription", "Settings"]
            )
        else:
            return st.sidebar.radio("Navigation", ["Login", "Register"])
