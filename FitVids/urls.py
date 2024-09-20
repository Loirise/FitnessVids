from django.urls import path
from .views import VideoUploadView, UserSignUpView, UserLoginView, FrontPageView, VideoListView, UserLogoutView

urlpatterns = [
    path('', FrontPageView, name='frontpage'),
    path('videos/', VideoListView, name='video_list'),
    path('upload/', VideoUploadView, name='video_upload'),
    path('login/', UserLoginView, name='login_page'),
    path('register/', UserSignUpView, name='register_page'),
    path('logout', UserLogoutView, name = 'logout_page')
]