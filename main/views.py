from django.shortcuts import render
from django.http import JsonResponse
from transformers import pipeline

# Home page
def home(request):
    return render(request, 'index.html')


from transformers import pipeline
from django.http import JsonResponse

# Load TinyLlama model
chatbot_ai = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)

def chatbot(request):

    # Get message
    message = request.GET.get('message', '').strip()

    # Lowercase version
    lower_msg = message.lower()

    # Greetings
    if lower_msg in ["hello", "hi", "hey"]:

        return JsonResponse({
            'reply': "Hello 👋 How can I help you today?"
        })

    # Family questions
    elif any(word in lower_msg for word in [
        "family",
        "fam",
        "brother",
        "sister",
        "parents"
    ]):

        return JsonResponse({
            'reply': "No, I am an AI assistant, so I do not have a real family."
        })

    # Identity
    elif "who are you" in lower_msg:

        return JsonResponse({
            'reply': "I am an AI chatbot designed to help users."
        })

    # Creator
    elif "created" in lower_msg or "creator" in lower_msg:

        return JsonResponse({
            'reply': "I was created using Python, Django, and AI technologies."
        })

    # News/live updates
    elif any(word in lower_msg for word in [
        "news",
        "war",
        "live",
        "today",
        "update"
    ]):

        return JsonResponse({
            'reply': "I currently do not have live internet access for real-time news updates."
        })

    # Prompt
    prompt = f"""
<|user|>
{message}

<|assistant|>
"""

    # Generate AI response
    result = chatbot_ai(

        prompt,

        max_new_tokens=80,

        temperature=0.5,

        top_k=50,

        top_p=0.9,

        repetition_penalty=1.2,

        do_sample=True
    )

    # Extract generated text
    text = result[0]['generated_text']

    reply = text.split("<|assistant|>")[-1].strip()

    # Remove unwanted tokens
    reply = reply.replace("<|user|>", "")
    reply = reply.replace("</s>", "")

    # Clean incomplete sentence
    if "." in reply:
        reply = reply.rsplit(".", 1)[0] + "."

    # Empty fallback
    if not reply:
        reply = "Sorry, I could not understand that properly."

    return JsonResponse({
        'reply': reply
    })








from django.http import JsonResponse
from diffusers import StableDiffusionPipeline
import torch
import os
from django.conf import settings

# Load AI Image Model
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32
)

# Image Generator
def generate_image(request):

    prompt = request.GET.get('prompt', '')

    if not prompt:
        return JsonResponse({
            'result': 'Please enter a prompt'
        })

    # Generate image
    image = pipe(prompt).images[0]

    # Media folder
    media_path = os.path.join(settings.MEDIA_ROOT, "generated_image.png")

    # Save image
    image.save(media_path)

    return JsonResponse({
        'image_url': settings.MEDIA_URL + "generated_image.png"
    })