from django.db import models
import random
import string

class User(models.Model):
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10, unique=True)
    otp = models.CharField(max_length=4, blank=True, null=True)

    def generate_otp(self):
        self.otp = f"{random.randint(1000, 9999)}"
        self.save()

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    table_name = models.CharField(max_length=255, unique=True)  # Increase max_length to 255
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.table_name:
            self.table_name = 'tbl_' + ''.join(random.choices(string.digits, k=10))
        super().save(*args, **kwargs)
