import io
import requests
import numpy
from PIL import Image
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
from transformers import CLIPVisionModel, CLIPImageProcessor

# Load models (you should do this at bot initialization)
model_id = "runwayml/stable-diffusion-v1-5"
scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler)

vision_model = CLIPVisionModel.from_pretrained("openai/clip-vit-base-patch32")
image_processor = CLIPImageProcessor.from_pretrained("openai/clip-vit-base-patch32")

async def generate_image(ctx):
    if len(ctx.message.attachments) == 0:
        await ctx.send("Please attach an image to your command.")
        return

    attachment = ctx.message.attachments[0]
    image_url = attachment.url
    
    # Download the image
    response = requests.get(image_url)
    image = Image.open(io.BytesIO(response.content)).convert("RGB")
    
    # Process the image with IP-Adapter
    inputs = image_processor(images=image, return_tensors="pt")
    image_features = vision_model(**inputs).last_hidden_state
    
    # Generate new image
    prompt = "A beutiful person"
    image = pipe(prompt=prompt, image=image_features).images[0]
    
    # Save and send the image
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    
    await ctx.author.send(file=discord.File(buffer, filename='generated_image.png'))
    await ctx.send(f"{ctx.author.mention}, I've sent you the generated image in a private message!")