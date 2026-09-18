import requests
import streamlit as st

st.set_page_config(page_title="AYORAI Vision Intelligence", layout="wide")
st.title("AYORAI Vision Intelligence")
st.caption("Computer Vision • Tracking • Confidence • Human-in-the-Loop • MCP • RAG")

api = st.sidebar.text_input("API URL", "http://api:8000")
file = st.file_uploader("Upload a video", type=["mp4","mov","avi","mkv"])

if st.button("Process video", disabled=file is None):
    with st.spinner("Running detection and tracking..."):
        response = requests.post(
            f"{api}/process-video",
            files={"file": (file.name, file.getvalue(), file.type)},
            timeout=1800,
        )
    if response.ok:
        st.success("Processing completed")
        data = response.json()
        st.json(data)
        if data.get("tracks"):
            st.subheader("Track summaries")
            st.dataframe(data["tracks"], use_container_width=True)
    else:
        st.error(response.text)

if st.button("Refresh tracks"):
    response = requests.get(f"{api}/tracks", timeout=30)
    st.json(response.json())
