from django import forms 
from .models import ImageUploader
from django.core.files import File
from PIL import Image

class ImageForm(forms.ModelForm): 
  
    class Meta: 
        model = ImageUploader 
        fields = ['image']


