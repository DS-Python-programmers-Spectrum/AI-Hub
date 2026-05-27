from django.db import models
from django.contrib.auth.models import User


# ==========================================
# CHAT HISTORY
# ==========================================

class ChatHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    user_message = models.TextField()

    bot_reply = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.user_message


# ==========================================
# GENERATED IMAGES
# ==========================================

class GeneratedImage(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    prompt = models.TextField()

    image = models.ImageField(
        upload_to='generated_images/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.prompt


# ==========================================
# GENERATED CODE
# ==========================================

class GeneratedCode(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    prompt = models.TextField()

    code = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.prompt


# ==========================================
# LEARNING RECOMMENDATIONS
# ==========================================

class LearningRecommendation(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    topic = models.CharField(
        max_length=200
    )

    level = models.CharField(
        max_length=100
    )

    recommendation = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.topic