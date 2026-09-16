# Data_Insight_Agent
An AI-powered data insights agent built on **Coze** and implemented with **Python + LangChain**, powered by the **DeepSeek** large language model, with **SQLite** as the data store and **Streamlit** as the chat-based frontend.

## Demo
### Initial Interface:
<img width="1920" height="1021" alt="image" src="https://github.com/user-attachments/assets/493aae3f-3a7b-49ac-9aa8-b693d61c6c67" />

### User query: "Show me product sales for February 2026" —> the agent converts natural language into SQL, queries the SQLite database, and returns the results.

<img width="1920" height="1015" alt="image" src="https://github.com/user-attachments/assets/fb65e271-5809-4529-9def-0155d300662f" />

### User query: "Give me a pie chart please" —> the agent uses context to link to the previous query and generates a pie chart of product sales for February 2026.

<img width="1920" height="1015" alt="image" src="https://github.com/user-attachments/assets/8c2e5258-4c26-4edb-8293-3a51936e7712" />

### User query: "Show me the sales trend for AirPods Pro from January to March, with a bar chart please" —> the agent generates SQL to retrieve monthly sales, calculates month-over-month growth, and generates a bar chart.

<img width="1920" height="1016" alt="image" src="https://github.com/user-attachments/assets/0d87cd62-db81-48c4-a396-75be459f78a8" />
<img width="1920" height="1015" alt="image" src="https://github.com/user-attachments/assets/d76107dc-7735-4119-a8f3-c05050d38ba8" />

## Core Features
-Natural language to SQL query generation for sales data

-Autonomous tool-calling via ReAct loop (Thought → Action → Observation)

-Automated mathematical calculation and result summarization

-Chart generation: bar, pie, scatter, line

-Multi-turn conversation with context memory

-Streamlit chat-based web interface with sidebar documentation


## Tech Stack: Coze, DeepSeek API, LangChain, SQLite, Streamlit

## How to Run:
### Before running: copy '.env.example' to '.env' and fill in your DeepSeek API key.
```bash
python -m venv .venv            # Create virtual environment
.venv\Scripts\activate          # Windows:activate virtual environment
source .venv/bin/activate       # Mac/Linux:activate virtual environment
pip install -r requirements.txt # Install dependencies
streamlit run app.py            # run the app
```
