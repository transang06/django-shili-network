from django.urls import path
from chat import views

app_name = 'chat'
urlpatterns = [
    path('', views.BoxChat.as_view(), name='box'),
    path('save_mess/', views.SaveMess.as_view(), name='save_mess'),
    path('delete_mess/', views.DeleteMess.as_view(), name='delete_mess'),
]