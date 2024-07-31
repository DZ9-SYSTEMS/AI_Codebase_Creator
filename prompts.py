# prompts.py

task_specifier_prompt = (
        """Here is a task that {assistant_role_name} will help {user_role_name} to complete: {task}.
    Please make it more specific.
    Please reply with the specified task in {word_limit} words or less. Do not add anything else."""
    )