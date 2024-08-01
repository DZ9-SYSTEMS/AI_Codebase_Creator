# tools.py

import os
from langchain.tools import Tool


def create_folder(folder_path: str) -> str:
    """
    Create a folder at the specified path.
    """
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder '{folder_path}' created successfully.")
        return f"Folder '{folder_path}' created successfully."
    except Exception as e:
        print(f"Failed to create folder '{folder_path}': {e}")
        return f"Failed to create folder '{folder_path}': {e}"

create_folder_tool = Tool(
    name="CreateFolderTool",
    func=create_folder,
    description="Create a folder at the specified path."
)

def create_file(file_path: str, content: str = "") -> str:
    """
    Create a file at the specified path with optional content.
    """
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"File '{file_path}' created successfully with content: {content}")
        return f"File '{file_path}' created successfully with content: {content}"
    except Exception as e:
        print(f"Failed to create file '{file_path}': {e}")
        return f"Failed to create file '{file_path}': {e}"

create_file_tool = Tool(
    name="CreateFileTool",
    func=create_file,
    description="Create a file at the specified path with optional content."
)
