from django.urls import path, include
from frontend import views

urlpatterns = [
    path('', views.index)
]
