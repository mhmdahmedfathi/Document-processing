from rest_framework import serializers
from .models import Image,PDFS
from drf_extra_fields.fields import Base64ImageField,Base64FileField
import PyPDF2
import io
import logging 
    

# Helpers

class PDFBase64File(Base64FileField):
    ALLOWED_TYPES = ['pdf']

    def get_file_extension(self, filename, decoded_file):
        try:
            PyPDF2.PdfReader(io.BytesIO(decoded_file))
        except PyPDF2.errors.PdfReadError:
            return False
        else:
            return 'pdf'
   

# Serializers to the media    

class ImageSerializer(serializers.ModelSerializer):

    file_encode = Base64ImageField(required=False)
    class Meta:
        model = Image
        fields = ["title", "description", "file_encode",'pk']


class PDFSerializer(serializers.ModelSerializer):

    file_encode = PDFBase64File(required=False)
    class Meta:
        model = PDFS
        fields = ["title", "description", "file_encode",'pk']