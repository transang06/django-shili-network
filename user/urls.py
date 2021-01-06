from django.urls import path
from user import views

app_name = 'user'
urlpatterns = [
    path('add_follow/', views.Add_follow.as_view(), name='add_follow'),
    path('alluser/', views.AllUser.as_view(), name='all_user'),
    path('<str:user_username>', views.Profile.as_view(), name='profile'),
    path('', views.ProfileMain.as_view(), name='profile_main'),
    path('api/getprofile/', views.ApiGetProfile.as_view(), name='api_getprofile'),
    path('api/editprofile/', views.ApiEditProfile.as_view(), name='edit_profile'),
    path('api/editavbg/', views.Edit_av_bg.as_view(), name='edit_av_bg'),
    path('api/your_friend/', views.ApiYourFriend.as_view(), name='api_your_friend'),
]
