# -*- coding: utf-8 -*-
import os
os.environ["NO_PROXY"] = "localhost,127.0.0.1"
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
import sqlite3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('你的api_key请填这里')

latest_image = None

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key = os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0
)

@tool
def calculate(expression: str) -> str:
    """"计算数学表达式，支持加减乘除等运算"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f'计算错误,错误类型:{e}'

@tool
def search(sql: str) -> str:
    """查询销售数据表，表的字段有product：产品型号，category：产品类别，amount：产品价格，quantity：产品的销售数量，sale_date：产品销售日期"""
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return str(result)
    except Exception as e:
        return f'查询错误，错误原因{e}'
    finally:
        conn.close()

@tool
def drawpicture(picture_type: str, x: list, y: list, x_label: str, y_label: str) -> str:
    """画图，可以画bar：柱状图、scatter：散点图、pie：饼图和line：线，并将图片保存下来"""
    global latest_image
    if picture_type == "bar":
        plt.bar(x, y)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
    elif picture_type == "scatter":
        plt.scatter(x, y)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
    elif picture_type == "pie":
        plt.pie(y, labels=x)
    elif picture_type == "line":
        plt.plot(x, y)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
    else:
        return f'不支持画{picture_type}'
    temp_name = datetime.now().strftime("%Y%m%d_%H_%M_%S")
    my_picture = f"{temp_name}.png"
    plt.savefig(my_picture)
    latest_image = my_picture
    plt.close()
    return '已保存为图片'

tools = [calculate, search, drawpicture]

prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个数据分析助手，可以查询销售数据库并进行计算分析。
请根据用户问题，生成正确的SQL语句查询数据库，然后对结果进行分析和总结。
只有当用户需要图时才画图，其他时候不要调用drawpicture工具,一次只能生成一张图。
回答要用中文，清晰易懂。"""),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10)

#Streamlit Web
st.title("数据洞察Agent")

#Streamlit 侧边栏
with st.sidebar:
    st.markdown("### 数据表结构")
    st.markdown('''
    sales表：
    | 字段 | 说明 |
    |------|------|
    | id | 记录编号 |
    | product | 产品名称 |
    | category | 产品类别 |
    | amount | 产品价格 |
    | quantity | 产品销售数量 |
    | sale_date | 产品销售日期 |
    ''')
    st.markdown("### 🔧 支持功能")
    st.markdown('''
    1、查询26年1-3月份各类产品的价格、销量  
    2、对查询结果进行数学计算（如总销售额、增长率等）  
    3、画柱状图、饼形图、散点图、折线图  
    4、支持多轮对话，能结合上下文连续分析''')

    st.markdown("### 💬 示例问题")
    st.markdown('''
    1、2月份各类产品销售数据  
    2、3月份什么卖的最好？  
    3、请给我1月份产品销售数量的饼形图  ''')

#保存对话记录，只在初始化的时候执行一次
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史对话
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🧑 **用户**: {msg['content']}") #st.markdown：显示格式化文字
    else:
        st.markdown(f"🤖 **Agent**: {msg['content']}")
    if msg.get("image"):
        st.image(msg["image"]) #st.image：显示图片


def clear_input():
    st.session_state["pending_input"] = st.session_state["input"]
    st.session_state["input"] = ""

st.text_input("你的问题：", key="input", on_change=clear_input) #用户提交时，先执行on_change，再执行text_input

if "pending_input" in st.session_state and st.session_state["pending_input"]:  #st.session_state存储信息，本质上是个字典
    user_input = st.session_state["pending_input"]
    st.session_state["pending_input"] = ""

    # 存用户消息
    st.session_state.messages.append({"role": "user", "content": user_input, "image": None})

    # 转LangChain格式
    lc_history = []
    for msg in st.session_state.messages[:-1]:
        if msg["role"] == "user":
            lc_history.append(HumanMessage(content=msg["content"]))
        else:
            lc_history.append(AIMessage(content=msg["content"]))

    # 调用Agent
    latest_image = None
    result = agent_executor.invoke({"input": user_input, "chat_history": lc_history})

    # 存AI回复
    st.session_state.messages.append({"role": "assistant", "content": result["output"], "image": latest_image})

    st.experimental_rerun() #重新跑一次，渲染对话历史

if "pending_input" == "退出":
    st.markdown("👋 感谢使用，再见！")
    st.stop()
