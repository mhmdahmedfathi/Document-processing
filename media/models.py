from django.db import models
from django.core.validators import FileExtensionValidator

def upload_image(instance, filename):
    file_path = f"images/{instance.title}-{filename}"
    return file_path


class Image(models.Model):
    title = models.CharField(
        max_length=80, blank=False, null=False)
    description = models.TextField()
    file_encode = models.ImageField(upload_to=upload_image, blank=True, null=True)

    def __str__(self):
        return self.title
    

def upload_pdf(instance, filename):
    file_path = f"pdfs/{instance.title}-{filename}"
    return file_path


class PDFS(models.Model):
    title = models.CharField(
        max_length=80, blank=False, null=False)
    description = models.TextField()
    file_encode = models.FileField(upload_to=upload_pdf, blank=True, null=True, validators=[FileExtensionValidator(['pdf'])])

    def __str__(self):
        return self.title