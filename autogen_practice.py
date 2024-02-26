from typing import Dict, Union
from ..Config import config


from IPython import get_ipython
from IPython.display import display, Image

import autogen

#import os

llm_config = {
    "config_list": [{"model": "gpt-4", "api_key": config.OPENAI_API_KEY}],
}



# create an AssistantAgent named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config) 

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    },
)
# the assistant receives a message from the user_proxy, which contains the task description
chat_res = user_proxy.initiate_chat(
    assistant,
    message="""find the top 10 performing cryptos today and show me a graph with their log returns for the past month""",
    summary_method="reflection_with_llm",
)