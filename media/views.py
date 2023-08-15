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
        print(img.shape)
        img_details = {
            'image':img,
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
            return Response(serializer.data)
        
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
                image = Img.open(image.file_encode)
                image = image.rotate(angle)
            except:
                return Response(status=404)
            
            print(image)
            return HttpResponse(image,content_type="image/png")

     
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
            images[i].save(name + '.jpg')
            urls.append(name)

        return Response(urls)
    
    
