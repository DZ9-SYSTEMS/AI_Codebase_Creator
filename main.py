# main.py

import os
import openai
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from prompts import task_specifier_prompt
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain.schema import (AIMessage, HumanMessage, SystemMessage)
from helper_functions import get_sys_msgs, CAMELAgent
from tools import CreateFolderTool, CreateFileTool

# Load OpenAI API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Create models
task_specify_model = ChatOpenAI(temperature=0.2)
assistant_model = ChatOpenAI(temperature=0)
user_model = ChatOpenAI(temperature=0)

# Set Streamlit page config
st.set_page_config(page_title="Self-Reflecting Agents", page_icon="🔗", layout="wide")
st.header("LangChain: Self-Reflecting Agents 🤖🔗")

# Default values
base_path = "/Users/isaiahlove/Desktop/"
default_assistant_role_name = "Full Stack Javascript Developer"
default_user_role_name = "Project manager"
default_task = "Create a crm using react and typescript. You should create the necessary Project folder, file structure, components and code. You should provide the code for each file."
default_word_limit = 100

# Get user input
assistant_role_name = st.sidebar.text_input("Assistant Role Name", default_assistant_role_name)
user_role_name = st.sidebar.text_input("User Role Name", default_user_role_name)
specified_task = st.sidebar.text_area("Task", default_task)
word_limit = st.sidebar.number_input("Word Limit for Task Brainstorming", value=default_word_limit)

# Initialize the system messages
assistant_sys_msg, user_sys_msg = get_sys_msgs(assistant_role_name, user_role_name, specified_task)

# Create custom tools
create_folder_tool = CreateFolderTool()
create_file_tool = CreateFileTool()
tools = [create_folder_tool, create_file_tool]

# Create CAMEL agents with tools
assistant_agent = CAMELAgent(assistant_sys_msg, assistant_model, tools)
user_agent = CAMELAgent(user_sys_msg, user_model, tools)

# Task specific Agent
task_specifier_sys_msg = SystemMessage(content="You can make a task more specific.")
task_specifier_template = HumanMessagePromptTemplate.from_template(template=task_specifier_prompt)
task_specifier_msg = task_specifier_template.format_messages(
    assistant_role_name=assistant_role_name,
    user_role_name=user_role_name,
    task=specified_task,
    word_limit=word_limit
)[0]

stored_messages = [task_specifier_sys_msg]
specified_task_msg = task_specify_model.invoke([task_specifier_sys_msg, task_specifier_msg])
stored_messages.append(specified_task_msg)

# Streamlit text output
st.subheader(f"Specified task:")
st.success(specified_task_msg.content)
specified_task = specified_task_msg.content

st.subheader("Conversation")
chat_turn_limit, n = 5, 0
prev_instructions = set()

while n < chat_turn_limit:
    n += 1
    user_ai_msg = user_agent.step(HumanMessage(content=f"Instruction {n}: {specified_task}"))
    user_msg = HumanMessage(content=user_ai_msg.content)

    # if user_msg.content in prev_instructions:
    #     user_msg.content += f" (variation {n})"
    # prev_instructions.add(user_msg.content)

    assistant_ai_msg = assistant_agent.step(user_msg)
    assistant_msg = HumanMessage(content=assistant_ai_msg.content)

    # Display the conversation in chat format
    st.text(f"AI User ({user_role_name}):")
    st.info(user_msg.content)
    st.text(f"AI Assistant ({assistant_role_name}):")
    st.success(assistant_msg.content)

    if "<CAMEL_TASK_DONE>" in user_msg.content:
        break
