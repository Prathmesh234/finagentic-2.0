from openai import OpenAI
import asyncio
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import base64
load_dotenv()



# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Getting the Base64 string


def analyze_image(file_path, task):
    
    model = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
    base64_image = encode_image(file_path)
    message = HumanMessage(
    content=[
        {"type": "text", "text": task},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{base64_image}"},
        },
    ],
    )
    response = model.invoke([message])
    return response.content

# Example usage

async def vision_agent(file_path, task):
    result = await asyncio.to_thread(analyze_image, file_path, task)
    print(result)



if __name__ == "__main__":
    file_path = r'resources\image.png'
    task="What is this image?"
    asyncio.run(vision_agent(file_path, task))