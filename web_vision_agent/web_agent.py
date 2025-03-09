from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
import json
import os 
import asyncio
import os 
import base64
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
from web_agent_instructions import MASTER_AGENT_NAME
from web_agent_instructions import MASTER_AGENT_INSTRUCTIONS
from semantic_kernel.contents import ImageContent, ChatMessageContent
import logging 

'''
The basic layout of the web agent is going to be as the following - 
1) We are going to build a chromium/selenium web driver plugin - done
2) Next we are going to take screenshots using omniparser 
3) These annotated screenshots are then going to be sent to azure ai inference for processing 
4) We are going to start with a prompt, get the website, navigate to the website, take a screenshot, use omni parser to annotate the screenshot and process using azure ai 
'''
'''
Agent 1 - Thinking agent -> drafting the entire plan (very simple steps to take to complete the task). Primary simple steps to complete the task and that's it. 
Step 1 - Initialize the browser (example)
mini agent - executes the step 2 and saves the screenshot after the step 2 into the resources folder
Step 2 - Navigate to the website (example)
mini agent - executes the step 2 and saves the screenshot after the step 2 into the resources folder
.....
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
    master_chat = ChatHistory()
    master_service_id = "master_agent"
    kernel.add_service(OpenAIChatCompletion(service_id= master_service_id, api_key=credentials, ai_model_id="gpt-4o"))
    master_settings = kernel.get_prompt_execution_settings_from_service_id(service_id= master_service_id)
    master_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    master_agent = ChatCompletionAgent(
        service_id="master_agent", kernel=kernel, name=MASTER_AGENT_NAME, instructions=MASTER_AGENT_INSTRUCTIONS, execution_settings=master_settings
    )
    master_reply = await invoke_agent(master_agent, user_query, master_chat)
    computer_use_service_id = "computer_use_agent"
    kernel.add_plugin(Computer_Use_Agent_plugin(), plugin_name="computer_use_plugin")
    kernel.add_service(OpenAIChatCompletion(service_id=computer_use_service_id, api_key=credentials, ai_model_id="gpt-4o"))
    computer_use_settings = kernel.get_prompt_execution_settings_from_service_id(service_id=computer_use_service_id)
    computer_use_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    computer_use_agent = ChatCompletionAgent(
    service_id="computer_use_agent", kernel=kernel, name=COMPUTER_USE_AGENT_NAME, instructions=COMPUTER_USE_AGENT_INSTRUCTIONS, execution_settings=computer_use_settings
    )
    try:
        if isinstance(master_reply, str):
            # Clean up the string if needed (remove code block markers if present)
            if "```json" in master_reply:
                master_reply = master_reply.split("```json")[1].split("```")[0].strip()
            elif "```" in master_reply:
                master_reply = master_reply.split("```")[1].split("```")[0].strip()
            
            plan_data = json.loads(master_reply)
        else:
            plan_data = master_reply
            
        # Extract the steps and create a numbered dictionary
        steps_dict = {i+1: step for i, step in enumerate(plan_data["steps"])}
        print(steps_dict)
        step_number=1
        while steps_dict[step_number] != "Task Complete":
            computer_use_agent_instruction = steps_dict[step_number]
            logger.info("Executing step %d: %s", step_number, computer_use_agent_instruction)
           
            agent_reply = await invoke_vision_agent(computer_use_agent, computer_use_agent_instruction, chat)
            logger.info("Agent reply: %s", agent_reply)
            if str(agent_reply) == "NOT COMPLETE":
                print("Task could not be completed. Please try again.")
                break
            elif str(agent_reply) == "NONE":
                print("Agent has been initiated.")
                agent_reply = await invoke_vision_agent(computer_use_agent, "INITIAL INSTRUCTION COMPLETED" + computer_use_agent_instruction, chat)
                ###LAST ERROR -> THE AGENT IS NOT INCREMENTING THE STEP NUMBER
            elif str(agent_reply) == "COMPLETE":
                print(f"step_number completed successfully.")
                step_number += 1
    except json.JSONDecodeError as e:
        logger.error("Error decoding JSON from master agent: %s", e)
        logger.error("Raw response was: %s", master_reply)
        raise
    step_number = 1

    ##Now we will execute the steps in the dict step by step
    
    



async def invoke_agent(agent: ChatCompletionAgent, input: str, chat: ChatHistory) -> str:
    """Invoke the agent with the user input."""
    logger.info("Invoking agent with input: %s", input)
    if isinstance(input, dict):
        clean_content = json.dumps(input)
    else:
        clean_content = str(input)
        clean_content = clean_content.replace(":True", ":true").replace(":False", ":false")
        chat.add_message({
            "role": "user",
            "content": clean_content
        })
    logger.info("User message added to chat history: %s", clean_content)
    print(f"# {AuthorRole.USER}: '{input}'")
    
    last_content = None
    async for content in agent.invoke(chat):
        logger.info("Agent response: %s", content.content)
        print(f"# {content.role} - {content.name or '*'}: '{content.content}'")
        last_content = content.content
        if isinstance(content.content, dict):
            clean_content = json.dumps(content.content)
        else:
            clean_content = str(content.content)
            clean_content = clean_content.replace(":True", ":true").replace(":False", ":false")
            chat.add_message({
                "role": content.role,
                "content": clean_content
            })
    
    # Return the content as a string instead of trying to parse it as JSON
    return last_content


async def invoke_vision_agent(agent: ChatCompletionAgent, input: str, chat: ChatHistory) -> str:
    """Invoke the agent with the user input."""
    logger.info("Invoking agent with input: %s", input)
    if isinstance(input, dict):
        clean_content = json.dumps(input)
    else:
        clean_content = str(input)
        clean_content = clean_content.replace(":True", ":true").replace(":False", ":false")
        image_path="resources/image.png"
        screenshot_uri=image_to_base64(image_path)
        image_content = ImageContent(data_uri=screenshot_uri, data_format="base64")
        chat.add_message({
            "role": "user",
            "content": clean_content
        })
        chat.add_message(
            ChatMessageContent(
                role="user",
                items=[image_content]
            )
        )
    logger.info("User message added to chat history: %s", clean_content)
    print(f"# {AuthorRole.USER}: '{input}'")
    
    last_content = None
    async for content in agent.invoke(chat):
        logger.info("Agent response: %s", content.content)
        print(f"# {content.role} - {content.name or '*'}: '{content.content}'")
        last_content = content.content
        if isinstance(content.content, dict):
            clean_content = json.dumps(content.content)
        else:
            clean_content = str(content.content)
            clean_content = clean_content.replace(":True", ":true").replace(":False", ":false")
            image_path="resources/image.png"
            screenshot_uri=image_to_base64(image_path)
            image_content = ImageContent(data_uri=screenshot_uri, data_format="base64")
            chat.add_message({
                "role": content.role,
                "content": clean_content
            })
            chat.add_message(
            ChatMessageContent(
                role="user",
                items=[image_content]
            )
        )
    
    # Return the content as a string instead of trying to parse it as JSON
    return last_content

import base64
import os

def image_to_base64(file_path: str) -> str:
    """
    Convert an image file to a base64-encoded string.
    
    Args:
        file_path (str): Path to the image file.
        
    Returns:
        str: Base64-encoded string of the image, prefixed with data URI scheme.
        
    Raises:
        FileNotFoundError: If the image file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Image file not found at {file_path}")
    
    with open(file_path, "rb") as image_file:
        # Read the binary content of the image
        image_data = image_file.read()
        # Encode to base64
        base64_encoded = base64.b64encode(image_data).decode("utf-8")
        # Determine the MIME type (assuming PNG for now; adjust if needed)
        mime_type = "image/png"  # You could use mimetypes.guess_type(file_path) for dynamic detection
        # Return with data URI scheme
        return f"data:{mime_type};base64,{base64_encoded}"

def main():
    asyncio.run(web_agent("Open edge browser and search for - 2024 USA Elections results and tell me the top news."))


if __name__ == "__main__":
    main()









