from django.db import models
import os
import shutil
import mysite.settings as settings

# Create your models here.
def path_file():
        def wrapper(user,filename):
            file_upload_dir = os.path.join(settings.MEDIA_ROOT, 'images')
            print(file_upload_dir)
            if os.path.exists(file_upload_dir):
                import shutil
                shutil.rmtree(file_upload_dir)
            return os.path.join(file_upload_dir, filename)
        return wrapper

class ImageUploader(models.Model):
    image = models.ImageField(blank = False, null = True,upload_to = path_file())


class Prediction(models.Model):
    uploaded_image = models.ImageField(blank = True, null = True)
    predicted_class = models.CharField(max_length = 250)


    