from django.db import models
from users.models import MyUser
from PIL import Image
# Create your models here.
# from sorl.thumbnail import ImageField, get_thumbnail

class Videomodel(models.Model):
    video=models.FileField(upload_to='video')
    content=models.CharField(max_length=255)
    logo=models.ImageField(upload_to='images/logo')
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.content+' '+str(self.id)
    

    def save(self, *args, **kwargs):
        super(Videomodel, self).save(*args, **kwargs)
        if self.logo:
            logo = Image.open(self.logo.path)
            output_size = (100, 100)
            logo = logo.resize(output_size)
            logo.save(self.logo.path)
