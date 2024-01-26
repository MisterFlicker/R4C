from django.urls import path
from . import views

urlpatterns = [
    path('', views.robots, name='robots'),
    path('report/', views.report, name='report'),
    path('uploaded_file/', views.upload_file, name='upload_file')
]
