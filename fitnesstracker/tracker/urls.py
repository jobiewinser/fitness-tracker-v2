from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('token', views.token, name='token'),
    path('exercise-catalogue', views.exercise_catalogue, name='exercise-catalogue'),
    path('exercise-detail/<str:pk>', views.exercise_detail, name='exercise-detail'),
    path('exercise-catalogue-search-results', views.exercise_catalogue_search_results, name='exercise-catalogue-search-results'),
    path('edit-workout/<str:pk>', views.EditWorkoutView.as_view(), name='edit-workout'),
    path('add-exercise-set/<int:previous_counter>', views.add_exercise_set, name='add-exercise-set'),
    path('add-exercise-super-set/<int:counter>', views.add_exercise_super_set, name='add-exercise-super-set'),
    path('add-exercise-super-set-button/<int:counter>', views.add_exercise_super_set_button, name='add-exercise-super-set-button'),
    
    path('support', views.support, name='support'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('exercise-create', views.ExerciseCreateView.as_view(), name='exercise-create'),
    path('workouts', views.workouts, name='workouts'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('sign-up', views.SignUpView.as_view(), name='sign-up'),
    
]