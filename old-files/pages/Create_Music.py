import streamlit as st
from st_audiorec import st_audiorec

wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    st.audio(wav_audio_data, format='audio/wav')

st.title("Create Music")
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "name" not in st.session_state:
    st.session_state["name"] = ""

if "user_ids" not in st.session_state:
    st.session_state["user_ids"] = []
if "names" not in st.session_state:
    st.session_state["names"] = []

user_id = st.number_input("User Id", st.session_state["user_id"])
name = st.text_input("Name",st.session_state["name"])
upload = st.button("Upload")

st.markdown("""
        <style>
            div[data-testid="column"] {
                width: fit-content !important;
                flex: unset;
            }
            div[data-testid="column"] * {
                width: fit-content !important;
            }
        </style>
        """, unsafe_allow_html=True)

st.text_area( label="",height=20, placeholder="Describe your music")
col1, col2 = st.columns([1,1])

with col1:
    listen = st.button('Listen')
with col2:
    post = st.button('Post')

if post:
    st.session_state["user_ids"].append(user_id)
    st.session_state["names"].append(name)
            
    