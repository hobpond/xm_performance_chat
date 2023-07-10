import os

from datetime import datetime, timezone
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder

from src.xm_group_tools import GroupDetailsTool, GroupPerformanceTool, OneGroupPerformanceTool
from src.xmapi import XMApi

# import langchain
# langchain.debug = True

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# larger context model works better but costs a lot more
# MODEL = "gpt-3.5-turbo-16k-0613"
MODEL = "gpt-3.5-turbo-0613"

MEMORY_KEY = "memory"

tools = [GroupPerformanceTool(), OneGroupPerformanceTool(), GroupDetailsTool()]
llm = ChatOpenAI(model_name = MODEL)
memory = ConversationBufferMemory(memory_key=MEMORY_KEY, return_messages=True)

# give the conversation memory the current date
memory.save_context({"input": "What is today's date?"},{"output": f"Today is {datetime.now(timezone.utc)}"})
memory.save_context({"input": "Main attribute of performance is the ratio of response and the lowest time to first response?"},{"output": f""})
memory.save_context({"input": "timeToFirstResponse is in milliseconds."},{"output": f""})

agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name = MEMORY_KEY)],
    "temperature": 0
}

agent_chain = initialize_agent(
    tools,
    llm,
    agent = AgentType.OPENAI_FUNCTIONS,
    verbose = True,
    agent_kwargs = agent_kwargs,
    memory = memory)

while True:
    user_input = input("User: ")
    if not user_input or user_input.lower() == "quit":
        break
    agent_chain.run(input = user_input)
