from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('exercise-catalogue', views.exercise_catalogue, name='exercise-catalogue'),
    path('exercise-detail/<str:pk>', views.exercise_detail, name='exercise-detail'),
    path('exercise-catalogue-search-results', views.exercise_catalogue_search_results, name='exercise-catalogue-search-results'),
    path('edit-workout/<str:workout_pk>', views.EditWorkoutView.as_view(), name='edit-workout'),
    path('add-exercise-set/<int:workout_pk>/<int:previous_counter>', views.add_exercise_set, name='add-exercise-set'),
    # path('add-exercise-super-set/<int:counter>', views.add_exercise_super_set, name='add-exercise-super-set'),
    # path('add-exercise-super-set-button/<int:counter>', views.add_exercise_super_set_button, name='add-exercise-super-set-button'),
    
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('exercise-create', views.ExerciseCreateView.as_view(), name='exercise-create'),
    path('workouts', views.workouts, name='workouts'),
    path('weighins', views.weighins, name='weighins'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('sign-up', views.SignUpView.as_view(), name='sign-up'),
    path('convert_weight_from_grams_htmx_handler/', views.convert_weight_from_grams_htmx_handler, name='convert_weight_from_grams_htmx_handler'),

    path('add-weighin/', views.AddWeighinView.as_view(), name='add-weighin'),
    path('delete_weigh_in/', views.delete_weigh_in, name='delete_weigh_in'),
    
]