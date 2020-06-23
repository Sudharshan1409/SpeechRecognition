"""
Urls.py includes the url configurations of the application.
"""

from django.urls import path

from App.views import Predict
from App.views import FileView
from App.views import FileDeleteView, RegisterUserPage, UpdateUserPage, AboutView, UpdateUserPage
from django.contrib.auth.views import LoginView,LogoutView

app_name = 'App'

urlpatterns = [
    path('predict/', Predict.as_view(), name='APIpredict'),
    path('upload/', FileView.as_view(), name='APIupload'),
    path('delete/', FileDeleteView.as_view(), name='APIdelete'),
    path('register/', RegisterUserPage.as_view(), name='register'),
    path('about/',AboutView.as_view(),name = 'about'),
    path('login/',LoginView.as_view(template_name = 'users/login.html'), name="login"),
    path('logout/',LogoutView.as_view(next_page = '/'),name = 'logout',kwargs = {'next_page':'/'}),
    path('update/<int:pk>',UpdateUserPage.as_view(),name = 'update'),
]
