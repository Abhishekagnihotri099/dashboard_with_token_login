import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import time
from auth import setup_authentication
from logging_utils import log_user_activity

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Homepage",
    page_icon="🌟",
    layout="wide"
)

st.markdown("""
    <style>
        body {
            background-image: url('https://via.placeholder.com/1920x1080');
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
            font-family: 'Arial', sans-serif;
        }
        .home-container {
            text-align: center;
            padding: 50px;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 15px;
            color: white;
            max-width: 80%;
            margin: auto;
        }
        .home-title {
            font-size: 4em;
            font-weight: bold;
            margin-bottom: 20px;
            text-shadow: 2px 2px 5px black;
        }
        .home-description {
            font-size: 1.8em;
            margin-bottom: 40px;
            text-shadow: 1px 1px 3px black;
        }
        .metric-card {
            background: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 12px;
            color: white;
            width: 300px;
            margin: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.6);
            display: flex;
            flex-direction: column;
            align-items: center;  /* Center align content inside card */
        }
        .metric-card-description {
            font-size: 1.2em;
            margin-top: 10px;
        }
        .stButton>button {
            background: linear-gradient(90deg, #ff7f50 0%, #ff4500 100%);
            color: white;
            padding: 8px 16px;  /* Reduced padding */
            border-radius: 12px;
            text-align: center;
            width: 90%;  /* Centered button within the card */
            font-size: 1em;  /* Reduced font size */
            font-weight: bold;
            border: none;
            box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.5);
            cursor: pointer;
            margin-top: 30px;  /* Space above the button */
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #ff4500 0%, #ff7f50 100%);
            color: #f0f8ff;
            box-shadow: 3px 3px 15px rgba(0, 0, 0, 0.7);
            transition: all 0.3s ease-in-out;
        }
    </style>
""", unsafe_allow_html=True)

# Home Page with Metric Cards
def home_page():
    username = st.session_state.get("username", "Unknown User")

    # # Log login only once
    # if not st.session_state.get("logged_in", False):
    #     log_user_activity(username, "Logged into Dashboard Home Page")
    #     st.session_state["logged_in"] = True
    #     st.session_state["logout_logged"] = False

    st.markdown("""
        <div class="home-container">
            <h1 class="home-title">Welcome to the EXL Dashboards</h1>
            <p class="home-description">Select a dashboard to explore insights and data visualization:</p>
        </div>
    """, unsafe_allow_html=True)



    # Creating 3 cards per row
    dashboard_info = [
        ("Claim Leakage Dashboard", "Description of Dashboard 1.", "Claim Leakage Dashboard"),
        ("Dashboard 2", "Description of Dashboard 2.", "dashboard2"),
        ("Dashboard 3", "Description of Dashboard 3.", "dashboard3"),
        ("Dashboard 4", "Description of Dashboard 4.", "dashboard4"),
        ("Dashboard 5", "Description of Dashboard 5.", "dashboard5"),
        ("Dashboard 6", "Description of Dashboard 6.", "dashboard6")
    ]

    # Create columns for the 3 cards per row
    for i in range(0, len(dashboard_info), 3):  # Create a row every 3 dashboards
        col1, col2, col3 = st.columns(3)

        with col1:
            if i < len(dashboard_info):
                title, description, dashboard = dashboard_info[i]
                if st.button(title, key=f"{title}_button"):
                    # st.session_state.page=dashboard
                    st.session_state["current_page"] = dashboard
                    st.query_params["user_data"] = dashboard
                    st.rerun()
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-card-description">
                            {description}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        with col2:
            if i+1 < len(dashboard_info):
                title, description, dashboard = dashboard_info[i+1]
                if st.button(title, key=f"{title}_button"):
                    st.session_state["current_page"] = dashboard
                    st.rerun()
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-card-description">
                            {description}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        with col3:
            if i+2 < len(dashboard_info):
                title, description, dashboard = dashboard_info[i+2]
                if st.button(title, key=f"{title}_button"):
                    st.session_state["current_page"] = dashboard
                    st.rerun()
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-card-description">
                            {description}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

def authenticate():
    authenticator = setup_authentication()

    # Centered Login Header with Image
    col1, col2, col3 = st.columns([3, 1, 3])  # Adjust column widths for better centering
    with col1:
        st.write("")  # Empty column for spacing
    with col2:
        st.image("exl.png", width=150)  # Ensure the file is in the same directory
    with col3:
        st.write("")

    # Authentication Login Logic
    try:
        col1, col2, col3 = st.columns([2, 2, 2])
        with col2:
            authenticator.login()
    except Exception as e:
        st.error(e)

    # Check Authentication Status
    if st.session_state.get('authentication_status', None):  # User is logged in
        username = st.session_state.get("username", "Unknown User")
        # Add Logout Button in Sidebar
        # with st.sidebar:
        #     st.markdown("###")
        #     if st.button("Logout"):
        #         authenticator.logout()
        #         # Clear all session state and rerun the app
        #         for key in st.session_state.keys():
        #             del st.session_state[key]  # Remove each session key
        #         st.rerun()  # Rerun the app after clearing state

        # Render the home page or other dashboard
        home_page()
        col1, col2, col3 = st.columns([2.8, 1.4, 2.8])
        with col2:
            authenticator.logout()
           


    elif st.session_state.get('authentication_status') is False:  # Invalid login
        col1, col2, col3 = st.columns([2, 2, 2])
        with col2:
            st.error("Username/password is incorrect")
        

    elif st.session_state.get('authentication_status') is None:  # Not logged in
        col1, col2, col3 = st.columns([2, 2, 2])
        with col2:
            st.warning("Please enter your username and password")
        


# Run the App
if __name__ == "__main__":
    authenticate()
