import streamlit as st

if st.session_state['authentication_status']:
    st.title("Dashboard 2")
    st.write("This is Dashboard 2")
else:
    st.warning("You must log in to access this page.")
    st.stop()

