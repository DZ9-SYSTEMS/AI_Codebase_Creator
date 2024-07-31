# tools.py

import os

class CreateFolderTool:
    def run(self, folder_path: str) -> str:
        """
        Create a folder at the specified path.
        """
        try:
            os.makedirs(folder_path, exist_ok=True)
            return f"Folder '{folder_path}' created successfully."
        except Exception as e:
            return f"Failed to create folder '{folder_path}': {e}"

class CreateFileTool:
    def run(self, file_path: str, content: str = "") -> str:
        """
        Create a file at the specified path with optional content.
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(content)
            return f"File '{file_path}' created successfully with content: {content}"
        except Exception as e:
            return f"Failed to create file '{file_path}': {e}"
