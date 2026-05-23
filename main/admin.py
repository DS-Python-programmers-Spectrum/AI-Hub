from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import *


admin.site.register(ChatHistory)

admin.site.register(GeneratedImage)

admin.site.register(GeneratedCode)