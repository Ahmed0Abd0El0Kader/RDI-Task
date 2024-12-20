
from django.urls import path , include
from .views import * 
urlpatterns = [
    # path('',index,name='index'),
    path('', upload_audio, name='upload_audio'),

]
