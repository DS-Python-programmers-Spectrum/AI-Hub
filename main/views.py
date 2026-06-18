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

    # User message
    message = request.GET.get('message', '').strip()

    if not message:

        return JsonResponse({
            'reply': 'Please enter a message.'
        })

    lower_msg = message.lower()

    # ==========================================
    # MANUAL REPLIES
    # ==========================================

    if lower_msg in ["hello", "hi", "hey"]:

        reply = "Hello 👋 How can I help you today?"

    elif "who are you" in lower_msg:

        reply = (
            "I am an AI assistant built using "
            "Django and Transformers."
        )

    elif "thank" in lower_msg:

        reply = "You're welcome 😊"

    elif "bye" in lower_msg:

        reply = "Goodbye 👋 Have a great day!"

    elif "llm" in lower_msg:

        reply = (
            "LLM stands for Large Language Model. "
            "It is an AI model trained on massive "
            "text data to understand and generate "
            "human language."
        )

    elif "machine learning" in lower_msg:

        reply = (
            "Machine Learning is a branch of AI "
            "that enables computers to learn from "
            "data and make predictions."
        )

    elif "deep learning" in lower_msg:

        reply = (
            "Deep Learning is a subset of machine "
            "learning that uses neural networks "
            "with multiple layers."
        )

    # ==========================================
    # AI GENERATED RESPONSE
    # ==========================================

    else:

        prompt = f"""
<|system|>
You are a smart AI assistant.

Rules:
- Give short and clear answers
- Maximum 2-3 sentences
- Avoid repetition
- Complete the answer properly

<|user|>
{message}

<|assistant|>
"""

        # Generate response
        result = chatbot_ai(

            prompt,

            max_new_tokens=45,

            temperature=0.4,

            top_k=40,

            top_p=0.85,

            repetition_penalty=1.3,

            do_sample=True,

            truncation=True
        )

        # Full generated text
        text = result[0]['generated_text']

        # Extract assistant reply
        reply = text.split("<|assistant|>")[-1]

        # Remove unwanted tokens
        reply = reply.replace("</s>", "")
        reply = reply.replace("<|user|>", "")
        reply = reply.replace("<|system|>", "")

        # Remove line breaks
        reply = reply.replace("\n", " ")

        # ==========================================
        # CLEAN RESPONSE
        # ==========================================

        sentences = reply.split(".")

        clean_reply = ""

        count = 0

        for sentence in sentences:

            sentence = sentence.strip()

            if sentence:

                clean_reply += sentence + ". "

                count += 1

            # Keep only first 2 sentences
            if count >= 2:
                break

        reply = clean_reply.strip()

        # Empty fallback
        if len(reply) < 2:

            reply = (
                "Sorry, I could not generate "
                "a proper response."
            )

    # ==========================================
    # SAVE CHAT HISTORY
    # ==========================================

    ChatHistory.objects.create(

        user=request.user,

        user_message=message,

        bot_reply=reply
    )

    # ==========================================
    # RETURN RESPONSE
    # ==========================================

    return JsonResponse({

        'reply': reply
    })
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
    GeneratedImage.objects.create(

    user=request.user,

    prompt=prompt,

    image=filename
)

    # Save database
    

    return JsonResponse({

        'image_url':

        settings.MEDIA_URL + filename
    })


# ==========================================
# CODE GENERATOR MODEL
# ==========================================



# ==========================================
# CODE GENERATOR FUNCTION
# ==========================================

from transformers import pipeline
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import GeneratedCode
import re

# ==========================================
# LOAD MODEL
# ==========================================

code_generator = pipeline(
    "text-generation",
    model="deepseek-ai/deepseek-coder-1.3b-instruct"
)


# ==========================================
# CODE GENERATOR
# ==========================================

@login_required(login_url="/login/")
def generate_code(request):

    prompt = request.GET.get("prompt", "").strip()

    if not prompt:
        return JsonResponse({
            "code": "Please enter a coding task."
        })

    lower_prompt = prompt.lower()

    # ==================================================
    # SMART PREDEFINED TEMPLATES
    # ==================================================

    if "calculator" in lower_prompt:

        code = """
<!DOCTYPE html>
<html>
<head>
<title>Calculator</title>

<style>

body{
    font-family:Arial;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    background:#0f172a;
}

.calculator{
    background:#1e293b;
    padding:20px;
    border-radius:15px;
    width:320px;
}

input{
    width:100%;
    height:55px;
    font-size:22px;
    text-align:right;
    margin-bottom:15px;
}

button{
    width:23%;
    height:55px;
    margin:2px;
    cursor:pointer;
}

</style>

</head>

<body>

<div class="calculator">

<input id="display" readonly>

<br>

<button onclick="add('7')">7</button>
<button onclick="add('8')">8</button>
<button onclick="add('9')">9</button>
<button onclick="add('/')">/</button>

<br>

<button onclick="add('4')">4</button>
<button onclick="add('5')">5</button>
<button onclick="add('6')">6</button>
<button onclick="add('*')">*</button>

<br>

<button onclick="add('1')">1</button>
<button onclick="add('2')">2</button>
<button onclick="add('3')">3</button>
<button onclick="add('-')">-</button>

<br>

<button onclick="add('0')">0</button>
<button onclick="calculate()">=</button>
<button onclick="clearDisplay()">C</button>
<button onclick="add('+')">+</button>

</div>

<script>

function add(value){

    document.getElementById("display").value += value;

}

function calculate(){

    try{

        document.getElementById("display").value =
        eval(document.getElementById("display").value);

    }

    catch{

        alert("Invalid Expression");

    }

}

function clearDisplay(){

    document.getElementById("display").value="";

}

</script>

</body>
</html>
"""

        GeneratedCode.objects.create(
            user=request.user,
            prompt=prompt,
            code=code
        )

        return JsonResponse({"code": code})

    # ==================================================
    # AI PROMPT
    # ==================================================

    full_prompt = f"""
You are an expert software engineer.

Generate ONLY source code.

Rules:

- Do not explain.
- Do not use markdown.
- Do not use ```html
- Do not use ```python
- Return complete working code.
- Use modern coding standards.
- If HTML is requested, include CSS and JavaScript.
- Never generate React JSX.
- Use class instead of className.
- Do not include comments outside the code.

Task:

{prompt}

Output:
"""

    # ==================================================
    # AI GENERATION
    # ==================================================

    result = code_generator(

        full_prompt,

        max_new_tokens=400,

        do_sample=False,

        eos_token_id=code_generator.tokenizer.eos_token_id,

        pad_token_id=code_generator.tokenizer.eos_token_id

    )

    generated = result[0]["generated_text"]

    code = generated.replace(full_prompt, "").strip()

    # ==================================================
    # CLEAN OUTPUT
    # ==================================================

    code = re.sub(r"```html", "", code, flags=re.IGNORECASE)
    code = re.sub(r"```python", "", code, flags=re.IGNORECASE)
    code = re.sub(r"```css", "", code, flags=re.IGNORECASE)
    code = re.sub(r"```javascript", "", code, flags=re.IGNORECASE)
    code = code.replace("```", "")

    code = code.replace("className=", "class=")

    code = code.replace("<|assistant|>", "")
    code = code.replace("</s>", "")

    code = code.replace("Here is the code:", "")
    code = code.replace("Here's the code:", "")

    code = code.strip()

    if len(code) < 20:
        code = "Unable to generate code. Please try a more specific prompt."

    # ==================================================
    # SAVE DATABASE
    # ==================================================

    GeneratedCode.objects.create(
        user=request.user,
        prompt=prompt,
        code=code
    )

    return JsonResponse({
        "code": code
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

# ==========================================
# PERSONALIZED DASHBOARD
# ==========================================

@login_required(login_url='/login/')
def dashboard(request):

    # Current logged-in user
    current_user = request.user

    # Only current user's chats
    chats = ChatHistory.objects.filter(

        user=current_user

    ).order_by('-id')[:10]

    # Only current user's images
    images = GeneratedImage.objects.filter(

        user=current_user

    ).order_by('-id')[:10]

    # Only current user's codes
    codes = GeneratedCode.objects.filter(

        user=current_user

    ).order_by('-id')[:10]

    # Dashboard stats
    total_chats = ChatHistory.objects.filter(

        user=current_user

    ).count()

    total_images = GeneratedImage.objects.filter(

        user=current_user

    ).count()

    total_codes = GeneratedCode.objects.filter(

        user=current_user

    ).count()

    # Personalized AI recommendation
    recommendation = ""

    if total_codes > 5:

        recommendation = (
            "💻 You are actively generating code. "
            "Try learning Django APIs and AI integrations."
        )

    elif total_images > 5:

        recommendation = (
            "🎨 You enjoy AI image generation. "
            "Explore prompt engineering and Stable Diffusion."
        )

    elif total_chats > 10:

        recommendation = (
            "🤖 You frequently use AI chat. "
            "Try building advanced AI assistants."
        )

    else:

        recommendation = (
            "🚀 Start exploring AI tools to get "
            "personalized recommendations."
        )

    # Send data to dashboard
    context = {

        'chats': chats,

        'images': images,

        'codes': codes,

        'total_chats': total_chats,

        'total_images': total_images,

        'total_codes': total_codes,

        'recommendation': recommendation
    }

    return render(

        request,

        'dashboard.html',

        context
    )

from .models import LearningRecommendation
@login_required(login_url='/login/')
def recommend_learning(request):

    topic = request.GET.get('topic', '').lower()

    if not topic:

        return JsonResponse({
            'recommendation': 'Please enter a topic.'
        })

    # Beginner Recommendations

    if "python" in topic:

        level = "Beginner"

        recommendation = """
1. Learn Python Basics
2. Learn Functions & OOP
3. Practice Mini Projects
4. Learn NumPy & Pandas
5. Start Machine Learning
"""

    elif "machine learning" in topic:

        level = "Intermediate"

        recommendation = """
1. Python & Statistics
2. NumPy & Pandas
3. Scikit-learn
4. Regression & Classification
5. ML Projects
"""

    elif "deep learning" in topic:

        level = "Advanced"

        recommendation = """
1. Neural Networks
2. TensorFlow / PyTorch
3. CNN
4. RNN & LSTM
5. Transformers
6. Build AI Projects
"""

    elif "django" in topic:

        level = "Beginner to Intermediate"

        recommendation = """
1. Python Basics
2. Django Models
3. Templates
4. Authentication
5. APIs
6. AI Integration
"""

    else:

        level = "General"

        recommendation = f"""
Recommended Path for {topic}:

1. Learn Basics
2. Watch Tutorials
3. Build Projects
4. Practice Daily
5. Create Portfolio
"""

    # Save to database
    LearningRecommendation.objects.create(

        user=request.user,

        topic=topic,

        level=level,

        recommendation=recommendation
    )

    return JsonResponse({

        'level': level,

        'recommendation': recommendation
    })