![Purple App Phone Mockup Sales Marketing Presentation](https://github.com/user-attachments/assets/2956de63-dc1b-4eea-a196-258b45c18989)

# Self-Reflecting Agents

A Streamlit application that demonstrates collaborative, role-based AI agents capable of self-reflection and tool use to accomplish complex software development tasks. Built with [LangChain](https://github.com/langchain-ai/langchain), OpenAI, and custom agent logic, this project enables an AI "Project Manager" and an AI "Developer" to work together to plan, create, and implement code projects.

## Features
- **Role-based AI agents**: Simulates a project manager and a developer collaborating on software tasks.
- **Self-reflection**: Agents can specify, clarify, and break down tasks for more effective execution.
- **Tool use**: Agents can create folders and files directly on your machine using custom tools.
- **Customizable roles and tasks**: Easily change agent roles and project requirements via the sidebar.
- **Interactive UI**: Built with Streamlit for a modern, responsive experience.

## Demo
Run the app and watch as the agents plan and generate code for a sample project, such as a CRM built with React and TypeScript.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Self_Reflecting_Agents
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   - Create a `.env` file in the project root with your OpenAI API key:
     ```env
     OPENAI_API_KEY=your-openai-api-key
     ```

## Usage

Start the Streamlit app:
```bash
streamlit run main.py
```

- Use the sidebar to set agent roles, specify the task, and adjust brainstorming word limits.
- Click **Submit Task** to watch the agents collaborate and generate solutions.

## Project Structure
- `main.py` — Streamlit app entry point; manages UI, agent setup, and conversation flow.
- `helper_functions.py` — Contains agent logic, message formatting, and tool invocation.
- `tools.py` — Custom tools for file and folder creation.
- `prompts.py` — Prompt templates for task specification.
- `inception_prompts.py` — System prompts for agent role behavior.
- `requirements.txt` — Python dependencies.

## Customization
- **Agent Roles**: Change the default roles in the sidebar or in `main.py`.
- **Base Path**: By default, files/folders are created on your Desktop. Change `DEFAULT_BASE_PATH` in `helper_functions.py` if needed.
- **Prompts**: Modify prompt templates in `prompts.py` and `inception_prompts.py` to experiment with agent behavior.

## Dependencies
- streamlit
- langchain
- openai
- streamlit-chat
- python-dotenv
- langchain-openai

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
