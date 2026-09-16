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
```bash
python -m venv .venv #create virtual environment
.venv\Scripts\activate        # Windows:activate virtual environment
source .venv/bin/activate     # Mac / Linux:activate virtual environment
pip install -r requirements.txt #Install dependencies
streamlit run app.py #run the app
```
