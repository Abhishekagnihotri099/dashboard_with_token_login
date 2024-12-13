from datetime import datetime
import plotly.graph_objects as go
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import time

def setup_authentication():
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Pre-hashing all plain text passwords once
    # stauth.Hasher.hash_passwords(config['credentials'])

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    return authenticator
    