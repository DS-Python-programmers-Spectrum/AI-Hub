from django.shortcuts import render
from django.http import JsonResponse

from transformers import pipeline

from diffusers import StableDiffusionPipeline

from .models import ChatHistory, GeneratedImage, GeneratedCode

from django.conf import settings

import torch

import os

import uuid

from django.contrib.auth.models import User

from django.contrib.auth import login

from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
# ==========================================
# HOME PAGE
# ==========================================

def home(request):

    return render(request, 'index.html')


# ==========================================
# CHATBOT MODEL
# ==========================================

chatbot_ai = pipeline(

    "text-generation",

    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)


# ==========================================
# CHATBOT FUNCTION
# ==========================================
@login_required(login_url='/login/')
def chatbot(request):

    # Get user message
    message = request.GET.get('message', '').strip()

    if not message:

        return JsonResponse({
            'reply': 'Please enter a message.'
        })

    # Lowercase message
    lower_msg = message.lower()

    # ==========================================
    # MANUAL REPLIES
    # ==========================================

    # Greetings
    if lower_msg in ["hello", "hi", "hey"]:

        reply = "Hello 👋 How can I help you today?"

    # Family
    elif any(word in lower_msg for word in [

        "family",
        "fam",
        "brother",
        "sister",
        "parents"
    ]):

        reply = "No, I am an AI assistant, so I do not have a real family."

    # Identity
    elif "who are you" in lower_msg:

        reply = "I am an AI chatbot designed to help users."

    # Creator
    elif "created" in lower_msg or "creator" in lower_msg:

        reply = "I was created using Python, Django, and AI technologies."

    # News
    elif any(word in lower_msg for word in [

        "news",
        "war",
        "live",
        "today",
        "update"
    ]):

        reply = "I currently do not have live internet access for real-time updates."

    # Joke
    elif "joke" in lower_msg:

        reply = "Why do programmers hate nature? Too many bugs 😄"

    # Thanks
    elif "thank" in lower_msg:

        reply = "You're welcome 😊"

    # Bye
    elif any(word in lower_msg for word in [

        "bye",
        "goodbye",
        "see you"
    ]):

        reply = "Goodbye 👋 Have a great day!"

    # ==========================================
    # AI GENERATED RESPONSE
    # ==========================================

    else:

        prompt = f"""
<|system|>
You are a smart, friendly AI assistant.

Rules:
- Answer clearly
- Keep answers short and natural
- Do not repeat sentences
- Do not pretend to have emotions or family
- Give meaningful responses

<|user|>
{message}

<|assistant|>
"""

        result = chatbot_ai(

            prompt,

            max_new_tokens=80,

            temperature=0.6,

            top_k=50,

            top_p=0.9,

            repetition_penalty=1.3,

            do_sample=True
        )

        text = result[0]['generated_text']

        reply = text.split("<|assistant|>")[-1].strip()

        # Remove unwanted text
        reply = reply.replace("<|user|>", "")
        reply = reply.replace("</s>", "")
        reply = reply.replace("<|system|>", "")

        # Clean repeated lines
        lines = reply.split("\n")

        clean_lines = []

        for line in lines:

            if line not in clean_lines:

                clean_lines.append(line)

        reply = " ".join(clean_lines)

        # Empty reply fallback
        if not reply:

            reply = "Sorry, I could not understand that properly."

    # ==========================================
    # SAVE CHAT HISTORY
    # ==========================================

    ChatHistory.objects.create(

        user_message=message,

        bot_reply=reply
    )

    return JsonResponse({
        'reply': reply
    })


# ==========================================
# IMAGE GENERATION MODEL
# ==========================================

pipe = StableDiffusionPipeline.from_pretrained(

    "stabilityai/sd-turbo",

    torch_dtype=torch.float32
)

pipe.to("cpu")


# ==========================================
# IMAGE GENERATOR
# ==========================================
@login_required(login_url='/login/')
def generate_image(request):

    prompt = request.GET.get('prompt', '').strip()

    if not prompt:

        return JsonResponse({
            'result': 'Please enter a prompt.'
        })

    # Generate image
    image = pipe(

        prompt,

        num_inference_steps=1,

        guidance_scale=0.0
    ).images[0]

    # Create media folder
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    # Unique image name
    filename = f"{uuid.uuid4()}.png"

    media_path = os.path.join(

        settings.MEDIA_ROOT,

        filename
    )

    # Save image
    image.save(media_path)

    # Save database
    GeneratedImage.objects.create(

        prompt=prompt,

        image=filename
    )

    return JsonResponse({

        'image_url':

        settings.MEDIA_URL + filename
    })


# ==========================================
# CODE GENERATOR MODEL
# ==========================================

code_generator = pipeline(

    "text-generation",

    model="deepseek-ai/deepseek-coder-1.3b-base"
)


# ==========================================
# CODE GENERATOR FUNCTION
# ==========================================

def generate_code(request):

    prompt = request.GET.get('prompt', '').strip()

    if not prompt:

        return JsonResponse({

            'code': 'Please enter a coding task.'
        })

    # AI Prompt
    full_prompt = f"""
Write clean and correct code for:

{prompt}

Code:
"""

    # Generate code
    result = code_generator(

        full_prompt,

        max_new_tokens=250,

        temperature=0.3,

        top_p=0.95,

        repetition_penalty=1.1,

        do_sample=True
    )

    generated = result[0]['generated_text']

    # Remove prompt
    code = generated.replace(full_prompt, "").strip()

    # Save database
    GeneratedCode.objects.create(

        prompt=prompt,

        code=code
    )

    return JsonResponse({

        'code': code
    })


# ==========================================
# SIGNUP
# ==========================================

def signup_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        email = request.POST.get('email')

        password = request.POST.get('password')

        # Check existing user
        if User.objects.filter(username=username).exists():

            return render(request, 'signup.html', {

                'error': 'Username already exists'
            })

        # Create user
        user = User.objects.create_user(

            username=username,

            email=email,

            password=password
        )

        login(request, user)

        return redirect('/dashboard/')

    return render(request, 'signup.html')

# ==========================================
# DASHBOARD
# ==========================================

@login_required
def dashboard(request):

    chats = ChatHistory.objects.all().order_by('-id')[:10]

    images = GeneratedImage.objects.all().order_by('-id')[:10]

    codes = GeneratedCode.objects.all().order_by('-id')[:10]

    context = {

        'chats': chats,

        'images': images,

        'codes': codes
    }

    return render(request, 'dashboard.html', context)