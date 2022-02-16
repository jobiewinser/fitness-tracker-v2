from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('token', views.token, name='token'),
    path('support', views.support, name='support'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('sign-up', views.SignUpView.as_view(), name='sign-up'),
    
]