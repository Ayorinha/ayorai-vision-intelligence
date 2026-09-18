import requests
import streamlit as st

st.set_page_config(page_title="AYORAI Vision Intelligence",page_icon="🤖",layout="wide")
st.title("AYORAI Vision Intelligence")
st.caption("Computer Vision • Tracking • Uncertainty • HITL • RAG • MCP • Agentic AI • RPA")

api=st.sidebar.text_input("API URL","http://api:8000")
tabs=st.tabs(["🎥 Jobs","🧑‍⚖️ Human Review","🧠 Agent","🔧 MCP"])

with tabs[0]:
    file=st.file_uploader("Upload a public/synthetic demo video",type=["mp4","mov","avi","mkv"])
    if st.button("Start processing",disabled=file is None):
        with st.spinner("Creating job..."):
            r=requests.post(f"{api}/jobs",files={"file":(file.name,file.getvalue(),file.type)},timeout=120)
        if r.ok:
            job_id=r.json()["job_id"]; st.session_state["job_id"]=job_id
            st.success(f"Job {job_id} queued.")
    job_id=st.session_state.get("job_id")
    if job_id:
        r=requests.get(f"{api}/jobs/{job_id}",timeout=30)
        if r.ok:
            st.json(r.json())
            d=requests.get(f"{api}/jobs/{job_id}/detections",timeout=30)
            if d.ok: st.dataframe(d.json(),use_container_width=True)

with tabs[1]:
    if st.button("Refresh review queue"):
        st.session_state["reviews"]=requests.get(f"{api}/reviews",timeout=30).json()
    for item in st.session_state.get("reviews",[]):
        st.write(f"Review #{item['id']} — {item['label']} — confidence {item['confidence']:.3f}")
        c1,c2=st.columns(2)
        if c1.button("Approve",key=f"a{item['id']}"):
            requests.post(f"{api}/reviews/{item['id']}",json={"decision":"APPROVED","reviewer":"dashboard"})
            st.rerun()
        if c2.button("Reject",key=f"r{item['id']}"):
            requests.post(f"{api}/reviews/{item['id']}",json={"decision":"REJECTED","reviewer":"dashboard"})
            st.rerun()

with tabs[2]:
    query=st.text_input("Ask about the system")
    if st.button("Run agent",disabled=not query):
        r=requests.post(f"{api}/agent/query",params={"query":query},timeout=30)
        st.json(r.json())

with tabs[3]:
    if st.button("List tools"):
        st.json(requests.get(f"{api}/tools",timeout=30).json())
    tool=st.text_input("Tool name")
    if st.button("Call tool",disabled=not tool):
        r=requests.post(f"{api}/mcp/call/{tool}",json={},timeout=30)
        st.json(r.json())
