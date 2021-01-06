from django.urls import path
from home import views

app_name = 'home'
urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('login/', views.Login_user.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.Register_user.as_view(), name='register'),
    path('sendpass/', views.Send_pass.as_view(), name='sendpass'),
    path('xacthuc/', views.Xac_thuc.as_view(), name='Xac_thuc'),
    path('xacthuc/<str:key>/<str:ban_ma>', views.Xacthuc.as_view(), name='xacthuc'),
    path('resetpassword/<str:key>/<str:ban_ma>', views.ResetPassword.as_view(), name='resetpassword'),
    path('check/', views.Check.as_view(), name='check'),
    # ==================
    path('api/get_content/', views.ApiGetContent.as_view(), name='api_get_content'),
]
