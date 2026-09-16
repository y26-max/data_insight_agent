## data_insight_agent
An AI-powered data insights agent built on Coze and implemented with Python + LangChain, powered by the DeepSeek large language model, with SQLite as the data store and Streamlit as the chat-based frontend.

## Core Features:
·Natural language to SQL query generation for sales data
·Autonomous tool-calling via ReAct loop (Thought → Action → Observation)
·Automated mathematical calculation and attribution analysis
·Chart generation: bar, pie, scatter, line
·Multi-turn conversation with context memory
·Streamlit chat-based web interface with sidebar documentation

## Tech Stack: DeepSeek API, LangChain, SQLite, Streamlit

## How to Run:
### Before running: copy .env.example to .env and fill in your DeepSeek API key.
'''bash
### 1. Create virtual environment
python -m venv .venv
### 2. Activate virtual environment
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac / Linux
### 3. Install dependencies
pip install -r requirements.txt
### 4. Run the app
streamlit run app.py
'''
