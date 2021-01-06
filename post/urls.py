from django.urls import path
from post import views

app_name = 'post'
urlpatterns = [
    path('', views.TopHashtagPost.as_view(), name='TopHashtagPost'),
    path('<int:post_id>/', views.ShowPost.as_view(), name='ShowPost'),
    path('edit/<int:post_id>/', views.EditPost.as_view(), name='edit'),
    path('set_post/', views.SetPost.as_view(), name='set_post'),
    path('delete/', views.DeletePost.as_view(), name='delete_post'),
    path('hashtag/<str:hashtag>', views.ApiHashtag.as_view(), name='api_hashtag_post'),
    path('hashtag/', views.TopHashtagPost.as_view(), name='TopHashtagPost'),
    path('comments/', views.Comment_post.as_view(), name='comments'),
    path('delete_comment/', views.Delete_comment.as_view(), name='delete_comment'),
    path('api/top_hashtag/', views.ApiTopHashtag.as_view(), name='top_hashtag'),
]
