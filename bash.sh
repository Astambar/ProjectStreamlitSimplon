#!/bin/bash
python3 -m venv .venv
source .venv/bin/activate
pip install streamlit
pip install pydantic
streamlit hello
source .venv/bin/activate