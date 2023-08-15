import datetime
from PIL import Image as Img
from django.http import HttpResponse
from .serializers import ImageSerializer,PDFSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Image,PDFS
from pdf2image import convert_from_path
from numpy import asarray
# Create your views here.


class FileUploadView(APIView):

    def post(self,request):
        # check if the file is an image or pdf
        extension = request.data['file_encode'].split(';')[0].split('/')[1]
        if extension == 'pdf':
            serializer = PDFSerializer(data=request.data)
        else:
            serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response(data=data)
        
        return Response(serializer.errors, status=400)
    

class ImageListView(APIView):

    def get(self,request):
        images = Image.objects.all()
        serializer = ImageSerializer(images,many=True)
        return Response(serializer.data)
    
class ImageDetailView(APIView):

    def get(self,request,pk):
        try:
            image = Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return Response(status=404)
        serializer = ImageSerializer(image)
        img = Img.open(image.file_encode)
        img = asarray(img)
        img_details = {
            'title':serializer.data['title'],
            'description':serializer.data['description'],
            'location':serializer.data['file_encode'],
            'height':img.shape[0],
            'width':img.shape[1],
            'channels':img.shape[2]
        }
        return Response(img_details)
    
    def delete(self,request,pk):
        try:
            image = Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return Response(status=404)
        image.delete()
        return Response(status=204)
    
class PDFListView(APIView):

    def get(self,request):
        pdfs = PDFS.objects.all()
        serializer = PDFSerializer(pdfs,many=True)
        return Response(serializer.data)
    
class PDFDetailView(APIView):
    
        def get(self,request,pk):
            try:
                pdf = PDFS.objects.get(pk=pk)
            except PDFS.DoesNotExist:
                return Response(status=404)
            serializer = PDFSerializer(pdf)
            # count the number of pages in the pdf
            pages = convert_from_path(pdf.file_encode.path)
            width, height = pages[0].size
            pdf_details = {
                'title':serializer.data['title'],
                'description':serializer.data['description'],
                'location':serializer.data['file_encode'],
                'pages':len(pages),
                'height':height,
                'width':width
            }
            return Response(pdf_details)
        
        def delete(self,request,pk):
            print(pk)
            try:
                pdf = PDFS.objects.get(pk=pk)
            except PDFS.DoesNotExist:
                return Response(status=404)
            pdf.delete()
            return Response(status=204)


class RotateImage(APIView):
    
        def post(self,request):
            id = request.data['id']
            angle = int(request.data['angle'])
            try:
                image = Image.objects.get(pk=id)
            except Image.DoesNotExist:
                return Response(status=404)
            # get the image from the path and rotate it
            try:
                image_PIL = Img.open(image.file_encode)
                image_PIL = image_PIL.rotate(angle)
            except:
                return Response(status=404)
            # save the image
            name =  image.file_encode.path.split('images')[0] + "rotated_image/" + \
                    image.file_encode.path.split('images')[1].split('.')[0] + datetime.datetime.now().strftime("%H%M%S%MS") \
                    + str(0) + ".PNG"
            image_PIL.save(name)
            url = {
                'url':name
            }
            return Response(status=200,data=url)

     
class PDFtoImageView(APIView):
    
    def post(self,request):
        id = request.data['id']
        try:
            pdf = PDFS.objects.get(pk=id)
        except PDFS.DoesNotExist:
            return Response(status=404)
        # convert the pdf to image and return the image
        images = convert_from_path(pdf.file_encode.path)
        urls = []
        for i in range(len(images)):
            # give it a dummy name
            name =  pdf.file_encode.path.split('pdfs')[0] + "converted_pdf/" + \
                    pdf.file_encode.path.split('pdfs')[1].split('.')[0] + datetime.datetime.now().strftime("%H%M%S%MS") \
                    + str(i) + ".jpg"
            images[i].save(name)
            urls.append(name)

        return Response(urls)
    
    
