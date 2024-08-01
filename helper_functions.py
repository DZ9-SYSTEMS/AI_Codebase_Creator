#helper_functions.py

from typing import List
import re
import os
from inception_prompts import assistant_inception_prompt, user_inception_prompt
from langchain.prompts.chat import SystemMessagePromptTemplate
from langchain.schema import BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from tools import create_folder_tool, create_file_tool

DEFAULT_BASE_PATH = "/Users/isaiahlove/Desktop/"

# Create System Messages
def get_sys_msgs(assistant_role_name: str, user_role_name: str, task: str):
    assistant_sys_template = SystemMessagePromptTemplate.from_template(
        template=assistant_inception_prompt
    )
    assistant_sys_msg = assistant_sys_template.format_messages(
        assistant_role_name=assistant_role_name,
        user_role_name=user_role_name,
        task=task,
    )[0]

    user_sys_template = SystemMessagePromptTemplate.from_template(
        template=user_inception_prompt
    )
    user_sys_msg = user_sys_template.format_messages(
        assistant_role_name=assistant_role_name,
        user_role_name=user_role_name,
        task=task,
    )[0]

    return assistant_sys_msg, user_sys_msg

# Define a class named CAMELAgent
class CAMELAgent:
    def __init__(
        self,
        system_message: SystemMessage,
        model: ChatOpenAI,
        tools: List[Tool] = None
    ) -> None:
        self.system_message = system_message
        self.model = model
        self.tools = tools if tools else []
        self.init_messages()

    def reset(self) -> None:
        self.init_messages()
        return self.stored_messages

    def init_messages(self) -> None:
        self.stored_messages = [self.system_message]

    def update_messages(self, message: BaseMessage) -> List[BaseMessage]:
        self.stored_messages.append(message)
        return self.stored_messages

    def step(self, input_message: HumanMessage) -> BaseMessage:
        messages = self.update_messages(input_message)
        output_message = self.model.invoke(messages)
        self.update_messages(output_message)
        self.invoke_tools(output_message.content)
        return output_message

    def invoke_tools(self, message_content: str):
        # Determine if the message is a command to create a folder or file
        if "create a folder at" in message_content:
            folder_path = self.extract_path(message_content)
            # Join the folder path with the default base path
            folder_path = os.path.join(DEFAULT_BASE_PATH, folder_path)
            print(f"create a folder at: {folder_path}")
            create_folder_tool.func(folder_path)
        print(f"message_content before create file if block: {message_content}")
        if "create a file at" in message_content:
            file_path, content = self.extract_file_details(message_content)
             # Join the folder path with the default base path
            filePath = os.path.join(DEFAULT_BASE_PATH, file_path)
            print(f"create a file at: {filePath}, content: {content}")
            create_file_tool.func(filePath, content)

    def extract_path(self, message_content: str) -> str:
        """
        Extract folder path from message content.
        Assumes message format: 'create folder at /path/to/folder'
        """
        match = re.search(r'create a folder at ([\S]+)', message_content)
        if match:
            return match.group(1)
        else:
            raise ValueError("Folder path not found in message content")

    def extract_file_details(self, message_content: str) -> tuple:
        """
        Extract file path and content from message content.
        Assumes message format: 'create file at /path/to/file with content: <content>'
        """
        print(f"extract_file_details | message_content: {message_content}")
        path_match = re.search(r'create a file at ([\S]+)', message_content)
        # content_match = re.search(r'with content: (.+)', message_content)
        content_match = re.search(r'```[\s\S]*?\n([\s\S]*?)```', message_content)
        if not content_match:
            content_match = re.search(r'with content\n([\s\S]*?)$', message_content.strip())
        print(f"path_match: {path_match}, content_match: {content_match}")
        if path_match and content_match:
            return path_match.group(1), content_match.group(1)
        else:
            if not path_match:
                raise ValueError(f"File path not found in message content")
            if not content_match:
                raise ValueError(f"File content not found in message content")

