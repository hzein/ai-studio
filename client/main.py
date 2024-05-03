import streamlit as st
from streamlit_jwt_authenticator import Authenticator

st.header("AI Studio")

# Your API url to get JWT token
api_url = "http://localhost:8000/auth/token"


authenticator = Authenticator(api_url)
# Add login form
authenticator.login()

"Session State:", st.session_state
print(st.session_state)

# Check user logged-in
if "access_token" in st.session_state:
    if st.session_state["access_token"]:
        # Write application content
        st.write("Content is available for logged-in users")
        # Add logout button
        authenticator.logout()

# # Check user logged-in
# if st.session_state["authentication_status"]:
#     # Write application content
#     st.write("Content is available for logged-in users")
#     # Add logout button
#     authenticator.logout()
