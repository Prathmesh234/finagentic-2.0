from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
import json
import os 
import asyncio
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from web_agent_instructions import COMPUTER_USE_AGENT_INSTRUCTIONS
from web_tools import Computer_Use_Agent_plugin
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.kernel import Kernel
from web_agent_instructions import COMPUTER_USE_AGENT_NAME
import logging 

'''
The basic layout of the web agent is going to be as the following - 
1) We are going to build a chromium/selenium web driver plugin - done
2) Next we are going to take screenshots using omniparser 
3) These annotated screenshots are then going to be sent to azure ai inference for processing 
4) We are going to start with a prompt, get the website, navigate to the website, take a screenshot, use omni parser to annotate the screenshot and process using azure ai 
'''

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def web_agent(user_query: str):
    ##this will be running our web agent 
    ## we will always starting with the user query 
    logger.info("Starting web agent with user query: %s", user_query)
    kernel = Kernel()
    load_dotenv(".env")
    chat = ChatHistory()
    credentials = os.getenv("OPENAI_API_KEY")
    computer_use_service_id = "computer_use_agent"
    kernel.add_plugin(Computer_Use_Agent_plugin(), plugin_name="computer_use_plugin")
    kernel.add_service(OpenAIChatCompletion(service_id=computer_use_service_id, api_key=credentials, ai_model_id="gpt-4o"))
    computer_use_settings = kernel.get_prompt_execution_settings_from_service_id(service_id=computer_use_service_id)
    computer_use_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    computer_use_agent = ChatCompletionAgent(
        service_id="computer_use_agent", kernel=kernel, name=COMPUTER_USE_AGENT_NAME, instructions=COMPUTER_USE_AGENT_INSTRUCTIONS, execution_settings=computer_use_settings
    )
    agent_reply = await invoke_agent(computer_use_agent, user_query, chat)
    logger.info("Agent reply: %s", agent_reply)
    print(agent_reply)
    



async def invoke_agent(agent: ChatCompletionAgent, input: str, chat: ChatHistory) -> None:
    """Invoke the agent with the user input."""
    if isinstance(input, dict):
             clean_content = json.dumps(input)
    else:
             clean_content = str(input)
             clean_content = clean_content.replace(":True", ":true").replace(":False", ":false")
             chat.add_message({
                "role": "user",
                "content": clean_content
                })
    print(f"# {AuthorRole.USER}: '{input}'")
    
    async for content in agent.invoke(chat):
        print(f"# {content.role} - {content.name or '*'}: '{content.content}'")
        type(content.content)
        if isinstance(content.content, dict):
             clean_content = json.dumps(content.content)
        else:
             clean_content = str(content.content)
             clean_content = clean_content.replace(":True", ":true").replace(":False", ":false")
             chat.add_message({
                "role": content.role,
                "content": clean_content
                })
       
    
    try:
        type(content.content)
        return json.loads(content.content)
        
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        raise

def main():
    asyncio.run(web_agent("Open edge browser and search for - 2024 USA Elections results and tell me the top news."))


if __name__ == "__main__":
    main()









