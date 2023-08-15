from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.FileUploadView.as_view()),
    path('images', views.ImageListView.as_view()),
    path('pdfs', views.PDFListView.as_view()),
    path('images/<int:pk>/', views.ImageDetailView.as_view()),
    path('pdfs/<int:pk>/', views.PDFDetailView.as_view()),
    path('convert-pdf-to-image/', views.PDFtoImageView.as_view()),
    path('rotate', views.RotateImage.as_view())
]