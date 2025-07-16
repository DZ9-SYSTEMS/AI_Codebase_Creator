import os
import openai
import streamlit as st
from dotenv import load_dotenv
import re
import time

# Load your OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Project Generator", layout="wide")
st.title("AI Project Generator")

# Sidebar UI for inputs
with st.sidebar:
    st.header("Project Settings")
    project_desc = st.text_area(
        "Describe your project (e.g., 'A CRM in React and TypeScript')",
        "A simple Node.js server application using Express. The project should have:\n- A package.json file\n- An index.js file that sets up the Express server\n- A routes/ folder with a users.js file for user-related routes\n- A public/ folder with an index.html file"
    )
    project_root = st.text_input("Project folder name", "simple-node-server")
    generate = st.button("Generate Project")

base_path = os.path.expanduser("~/Desktop")
project_path = os.path.join(base_path, project_root)

def sanitize_name(name):
    # Remove all tree drawing characters and whitespace
    name = re.sub(r'[\|\-─└├│]+', '', name)
    name = name.strip()
    name = re.sub(r'[<>:"/\\|?*]', '', name)  # Remove invalid filename chars
    return name

def parse_tree_to_paths(tree):
    # Parses a markdown tree into a list of relative file paths (with folders)
    paths = []
    stack = []  # (indent_level, folder_name)
    lines = [line for line in tree.splitlines() if line.strip() and not line.strip().startswith("```")]
    if not lines:
        return []
    # Skip the root folder line (first line)
    lines = lines[1:]
    for line in lines:
        clean = line.lstrip(" |-─└├│")
        indent = len(line) - len(line.lstrip(" "))
        clean = sanitize_name(clean)
        # If it's a folder (no dot, not a file)
        if "." not in clean:
            while stack and stack[-1][0] >= indent:
                stack.pop()
            stack.append((indent, clean))
        else:
            # Sanitize all parent folders as well
            folder_path = "/".join([sanitize_name(f[1]) for f in stack])
            rel_path = os.path.join(folder_path, sanitize_name(clean)) if folder_path else sanitize_name(clean)
            # Remove any accidental whitespace or %20 in the rel_path
            rel_path = rel_path.replace(" ", "").replace("%20", "")
            paths.append(rel_path)
    return paths

def display_tree_from_paths(paths, root_name):
    # Build a nested dict from paths
    tree = {}
    for path in paths:
        parts = path.split(os.sep)
        d = tree
        for part in parts[:-1]:
            d = d.setdefault(part, {})
        d[parts[-1]] = None
    # Recursively print the tree
    def print_tree(d, prefix=""):
        lines = []
        items = list(d.items())
        for i, (name, subtree) in enumerate(items):
            connector = "└── " if i == len(items) - 1 else "├── "
            lines.append(prefix + connector + name)
            if subtree:
                extension = "    " if i == len(items) - 1 else "│   "
                lines.extend(print_tree(subtree, prefix + extension))
        return lines
    return f"{root_name}\n" + "\n".join(print_tree(tree))

def extract_code_for_file(response_text, rel_path):
    import re
    filename = os.path.basename(rel_path)
    # Remove code block markers and language tags
    code = response_text.strip()
    # Remove all code block markers (``` or ```lang)
    code = re.sub(r"^```[a-zA-Z0-9]*\s*", "", code)
    code = re.sub(r"```$", "", code)
    # Remove filename comments (e.g., // index.js or <!-- index.html -->)
    code = re.sub(rf"^\s*//\s*{re.escape(filename)}\s*", "", code)
    code = re.sub(rf"^\s*<!--\s*{re.escape(filename)}\s*-->\s*", "", code)
    return code.strip()

if generate:
    # 1. Get file/folder structure
    prompt_tree = f"""
You are a senior software architect. Given the following project description, output the full file/folder structure as a tree (use markdown code block, no explanations):

Project: {project_desc}
Root folder: {project_root}
"""
    with st.spinner("Generating file/folder structure..."):
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt_tree}],
            temperature=0,
        )
        tree = response.choices[0].message.content
    # 2. Parse file paths from the tree (with folders, sanitized)
    file_paths = parse_tree_to_paths(tree)
    # 3. Display the sanitized project structure
    st.markdown("### Project Structure")
    st.markdown(f"```\n{display_tree_from_paths(file_paths, project_root)}\n```")

    # 4. For each file, get code and create file
    st.markdown("### Files and Code")
    os.makedirs(project_path, exist_ok=True)
    for rel_path in file_paths:
        abs_path = os.path.join(project_path, rel_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        prompt_code = f"""
You are a senior developer. Write ONLY the code for the file `{rel_path}` in a {project_desc} project. Do not include code for any other file. Do not include code block markers or filename comments. Only output the code, no explanations.
"""
        st.markdown(f"**`{rel_path}`**")
        code_placeholder = st.empty()
        code = ""
        with st.spinner(f"Generating code for {rel_path}..."):
            stream_resp = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt_code}],
                temperature=0,
                stream=True,
            )
            for chunk in stream_resp:
                if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                    code += chunk.choices[0].delta.content
                    code_placeholder.code(code, language=rel_path.split(".")[-1])
                    time.sleep(0.01)
        # Extract only the code for this file
        pure_code = extract_code_for_file(code, rel_path)
        with open(abs_path, "w") as f:
            f.write(pure_code)
        code_placeholder.code(pure_code, language=rel_path.split(".")[-1])

    st.success(f"Project created at: {project_path}")