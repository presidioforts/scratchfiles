# file: ui_troubleshooter.py
import streamlit as st
import requests
import json

API_URL = "http://localhost:8080/troubleshoot"

st.set_page_config(page_title="DevOps Break-Fix Assistant", page_icon="🛠")
st.title("🛠 DevOps Break-Fix Troubleshooting Assistant")

with st.form(key="troubleshoot_form"):
    query = st.text_area(
        "Describe the error or paste the log snippet:",
        height=120,
        placeholder="e.g. npm ERR! code ERESOLVE …"
    )
    submitted = st.form_submit_button("Search")

if submitted:
    if not query.strip():
        st.warning("Please enter a description.")
        st.stop()

    with st.spinner("Contacting troubleshoot API…"):
        try:
            res = requests.post(API_URL, json={"text": query}, timeout=10)
            res.raise_for_status()
            data = res.json()
        except requests.RequestException as exc:
            st.error(f"HTTP error: {exc}")
            st.stop()
        except json.JSONDecodeError:
            st.error("API did not return valid JSON.")
            st.stop()

    # Render the markdown response nicely
    st.markdown("---")
    st.markdown("### Suggested Resolution")
    st.markdown(data["response"], unsafe_allow_html=True)

    # Show similarity score
    st.metric("Similarity score", f"{data['similarity_score']:.3f}")

    # Optional: collapsible raw payload
    with st.expander("See raw response"):
        st.json(data)
