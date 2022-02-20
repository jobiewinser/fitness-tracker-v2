from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('token', views.token, name='token'),
    path('exercise-catalogue', views.exercise_catalogue, name='exercise-catalogue'),
    path('exercise-detail/<int:pk>', views.exercise_detail, name='exercise-detail'),
    path('support', views.support, name='support'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('exercise-create', views.ExerciseCreateView.as_view(), name='exercise-create'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('sign-up', views.SignUpView.as_view(), name='sign-up'),
    
]