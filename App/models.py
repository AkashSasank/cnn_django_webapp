from django.db import models

# Create your models here.


class Photo(models.Model):
    document = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document.name