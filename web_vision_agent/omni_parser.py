import asyncio
from gradio_client import Client, handle_file
from PIL import Image, ImageDraw
import ast

def initiate_parser(screenshot_path):
    """Synchronous function to get bounding box data from OmniParser."""
    client = Client("microsoft/OmniParser")
    result = client.predict(
        image_input=handle_file(screenshot_path),
        box_threshold=0.05,
        iou_threshold=0.1,
        api_name="/process"
    )
    return result

async def draw_boxes_async(screenshot_path, task):
    """Async function to draw bounding boxes on the image."""
    # Run initiate_parser in a separate thread
    result = await asyncio.to_thread(initiate_parser, screenshot_path)
    
    # Extract components from the result tuple
    image_path, _, boxes_string = result
    
    # Parse the boxes string into a dictionary
    boxes_dict = ast.literal_eval(boxes_string)
    
    # Load the image
    image = Image.open(image_path)
    width, height = image.size
    
    # Create a drawing object
    draw = ImageDraw.Draw(image)
    
    
    
    # Save the output image
    output_path = f"resources/{task}.png"
    image.save(output_path)
    print(f"Output saved to {output_path}")

async def get_omniparser_output(task):
    """Main async function to run the drawing process."""
    screenshot_path = 'resources/screenshot.png'
    await draw_boxes_async(screenshot_path, task)

if __name__ == "__main__":
    asyncio.run(get_omniparser_output(task="Get bounding boxes"))