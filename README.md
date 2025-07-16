https://github.com/user-attachments/assets/774b561c-8df5-4b72-9da0-baf695894553

# AI Codebase Creator

A modern Streamlit application that uses the OpenAI API to generate full project structures and code for any stack (Node.js, React, HTML/CSS/JS, etc.) in real time. The app features a sidebar UI for project settings, streaming code output, and robust file/folder creation directly on your Desktop.

## Features
- **OpenAI-powered project generation**: Describe your project and get a complete, ready-to-run codebase.
- **Sidebar UI**: Enter your project description and folder name in a clean, modern sidebar.
- **Streaming output**: Watch code for each file appear in real time as it's generated.
- **Robust file/folder creation**: All files and folders are created with clean names and correct structure.
- **No LangChain or agent logic**: Pure OpenAI API for maximum transparency and control.

## Demo
Run the app and watch as it generates a Node.js server, a React app, or any other project you describe. All code is shown in the UI and written to disk.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd AI_Codebase_Creator
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create a `.env` file in the project root with your OpenAI API key:
     ```env
     OPENAI_API_KEY=your-openai-api-key
     ```

## Usage

Start the Streamlit app:
```bash
streamlit run app.py
```

- Use the sidebar to set your project description and folder name.
- Click **Generate Project** to watch the structure and code appear in real time.
- All files and folders will be created on your Desktop in the specified folder.

## Project Structure
- `app.py` — Main Streamlit app (OpenAI-powered, no LangChain)
- `requirements.txt` — Python dependencies

## Customization
- **Project Description**: Describe any stack or architecture you want (Node.js, React, HTML/CSS/JS, etc.).
- **Folder Name**: Choose where your project will be created on your Desktop.
- **Prompts**: The app is prompt-driven and can be easily adapted for more advanced workflows.

## Dependencies
- streamlit
- openai
- python-dotenv

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
