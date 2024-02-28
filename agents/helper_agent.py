
import os

import autogen

llm_config = {
    "config_list": [{"model": "gpt-4-1106-preview", "api_key": os.OPENAI_API_KEY}],
}

# create an AssistantAgent named "dev_assistant"
dev_assistant = autogen.AssistantAgent(
    name="dev_assistant",
    llm_config=llm_config)

# create a UserProxyAgent instance named "developer_proxy"
developer_proxy = autogen.UserProxyAgent(
    name="developer_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "data",
        "use_docker": False,  # Assuming Docker is available for a safer execution environment.
    },
)

# the developer_proxy receives a message from the dev_assistant, which contains the task description for indexing the directory for model processing
chat_res = developer_proxy.initiate_chat(
    dev_assistant,
    message="""index the directory for model processing""",
    summary_method="reflection_with_llm",
)