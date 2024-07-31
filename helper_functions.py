# helper_functions.py

from typing import List, Any
from inception_prompts import assistant_inception_prompt, user_inception_prompt
from langchain.prompts.chat import SystemMessagePromptTemplate
from langchain.schema import BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from tools import CreateFolderTool, CreateFileTool

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
        tools: List[Any] = None  # Accept custom tools
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

        # Process custom tools before model call
        tool_result = None
        for tool in self.tools:
            if isinstance(tool, CreateFolderTool) and "Use CreateFolderTool" in input_message.content:
                folder_path = input_message.content.split("Use CreateFolderTool to create a folder at ")[1].strip()
                if folder_path:
                    tool_result = tool.run(folder_path)
                else:
                    tool_result = "No folder path specified."
            elif isinstance(tool, CreateFileTool) and "Use CreateFileTool" in input_message.content:
                parts = input_message.content.split("Use CreateFileTool to create a file at ")[1].split(" with content ")
                if len(parts) == 2:
                    file_path = parts[0].strip()
                    content = parts[1].strip()
                    if file_path:
                        tool_result = tool.run(file_path, content)
                    else:
                        tool_result = "No file path specified."
                else:
                    tool_result = "No file path or content specified."

            if tool_result:
                print(tool_result)

        output_message = self.model.invoke(messages)
        self.update_messages(output_message)

        return output_message
