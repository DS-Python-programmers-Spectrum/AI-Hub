from django.db import models

# Create your models here.
from django.db import models


# Chat History

class ChatHistory(models.Model):

    user_message = models.TextField()

    bot_reply = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.user_message


# Generated Images

class GeneratedImage(models.Model):

    prompt = models.TextField()

    image = models.ImageField(upload_to='generated_images/')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.prompt


# Generated Code

class GeneratedCode(models.Model):

    prompt = models.TextField()

    code = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.prompt