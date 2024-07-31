import os
from langchain.agents import tool

@tool
def create_folder(folder_path: str) -> str:
    """
    Create a folder at the specified path.
    """
    try:
        os.makedirs(folder_path)
        return f"Folder created at {folder_path}"
    except FileExistsError:
        return f"Folder already exists at {folder_path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@tool
def create_file(file_path: str, content: str = "") -> str:
    """
    Create a file at the specified path with optional content.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return f"File created at {file_path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


from langchain.tools import BaseTool
from math import pi
from typing import Union

class CreateFolderTool(BaseTool):
    name = "Create Folder"
    description = "use this tool when you need to create a folder"

    def _run(self, folder_path: str) -> str:
        """
        Create a folder at the specified path.
        """
        try:
            os.makedirs(folder_path)
            return f"Folder created at {folder_path}"
        except FileExistsError:
            return f"Folder already exists at {folder_path}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def _arun(self, radius: int):
        raise NotImplementedError("This tool does not support async")

class CreateFileTool(BaseTool):
    name = "Create File"
    description = "Use this tool when you need to create a file"

    def _run(self, file_path: str, content: str = "") -> str:
        """
        Create a file at the specified path with optional content.
        """
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            return f"File created at {file_path}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def _arun(self, radius: int):
        raise NotImplementedError("This tool does not support async")