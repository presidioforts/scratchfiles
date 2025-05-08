
source venv/bin/activate
gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080



import streamlit as st
import requests
import json

# Medium-width text area styling
st.markdown(
    """
    <style>
    textarea {
        width: 70% !important;
        margin-left: auto !important;
        margin-right: auto !important;
        display: block !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
