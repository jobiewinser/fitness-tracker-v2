from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework.views import APIView

from django.core.mail import EmailMessage
from django.db.models import Q
# class LoginView(TemplateView):
#     template_name = 'tracker/login.html'
#     def post(self, request):
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)

#         if user is not None:
#             if user.is_active:
#                 login(request, user)

#                 return HttpResponse('Success', 200)
#             else:
#                 return HttpResponse("Inactive user.", status=410)
#         else:
#             return HttpResponse("No user found with the entered credentials.", status=404)

class LoginView(SuccessMessageMixin, LoginView):
    template_name = 'tracker/login.html'
    success_url = "/"
    form_class = UserLoginForm
    success_message = "Successful Login"

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")

class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'tracker/register.html'
    success_url = "/"
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"

class ExerciseCreateView(SuccessMessageMixin, CreateView):
    template_name = 'tracker/exercise_create.html'
    success_url = "/"
    form_class = ExerciseCreateForm
    success_message = "Your exercise has been added"

    def post(self, request, *args, **kwargs):
        exercise = Exercise(name=request.POST['name'], alternative_names=request.POST['alternative_names'].split(','))
        exercise.save()
        try:
            for file in request.FILES.getlist('images'):
                image = ImageModel(image = file)
                image.save()
                exercise.images.add(image)
            exercise.save()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponse(status=500)
        
class ProfileView(SuccessMessageMixin, UpdateView):
    template_name = 'tracker/profile.html'
    success_url = "/"
    form_class = ProfileForm
    model = Profile
    success_message = "Your profile was edited successfully"

    def get_object(self, *args, **kwargs):
        return self.request.user.profile

    def get_success_url(self, *args, **kwargs):
        return reverse("index")

    def post(self, request, *args, **kwargs):
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.display_name=request.POST['display_name']
        profile.fav_colour=request.POST['fav_colour']
        profile.weight_unit=request.POST['weight_unit']

        profile.save()
        try:
            for file in request.FILES.getlist('pictures'):
                image = ImageModel(image = file)
                image.save()
                profile.pictures.add(image)
            profile.save()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponse(status=500)
def index(request):
    if request.user.is_authenticated:
        request.user.get_or_create_profile()
    return render(request, 'tracker/index.html')

def token(request):
    api_token = 'fake_token'
    if request.META.get("HTTP_HX_REQUEST") != 'true':
        # return redirect('index')
        return render(request, 'tracker/token_full.html', {'token': api_token})

    return render(request, 'tracker/token.html', {'token': api_token})

def support(request):
    if request.META.get("HTTP_HX_REQUEST") != 'true':
        return render(request, 'tracker/support_full.html')

    return render(request, 'tracker/support.html')

def exercise_catalogue(request):
    queryset = Exercise.objects.filter()
    if request.META.get("HTTP_HX_REQUEST") != 'true':
        # return redirect('index')
        return render(request, 'tracker/exercise_catalogue_full.html', {'exercises': queryset})

    return render(request, 'tracker/exercise_catalogue.html', {'exercises': queryset})


def exercise_catalogue_search_results(request):
    queryset = Exercise.objects.all()
    if 'search' in request.POST:
        queryset = queryset.filter(Q(name__icontains=request._post['search']) | Q(alternative_names__icontains=request._post['search']))
    return render(request, 'tracker/exercise_catalogue_search_results.html', {'exercises': queryset})

def exercise_detail(request, **kwargs):
    exercise = Exercise.objects.get(pk=kwargs['pk'])
    if request.META.get("HTTP_HX_REQUEST") != 'true':
        return render(request, 'tracker/exercise_detail_full.html', {'exercise': exercise})
    return render(request, 'tracker/exercise_detail.html', {'exercise': exercise})


def workouts(request, **kwargs):
    workouts = WorkOut.objects.filter(profile=request.user.profile)
    if request.META.get("HTTP_HX_REQUEST") != 'true':
        return render(request, 'tracker/workouts_full.html', {'workouts': workouts})
    return render(request, 'tracker/workouts.html', {'workouts': workouts})

def weighins(request, **kwargs):
    weighins = WeighIn.objects.filter(profile=request.user.profile).order_by('-recorded')
    if request.META.get("HTTP_HX_REQUEST") != 'true':
        return render(request, 'tracker/weighins_full.html', {'weighins': weighins})
    return render(request, 'tracker/weighins.html', {'weighins': weighins})




class EditWorkoutView(APIView):
    def get(self, request, **kwargs):
        try:
            workout = WorkOut.objects.get(pk=kwargs['workout_pk'], profile=request.user.profile)
        except:
            workout = WorkOut(profile=request.user.profile)

            if not workout.name:
                existing_unnamed_workout = WorkOut.objects.filter(profile=request.user.profile, name__in="Custom Workout")
            if existing_unnamed_workout:
                counter  = existing_unnamed_workout.count()
            else:
                counter = 1
            workout.name = f"Custom Workout - {counter}"
            workout.save()
            return HttpResponseRedirect(f'/edit-workout/{workout.pk}')
        exercises_queryset = Exercise.objects.all()
    
        if request.META.get("HTTP_HX_REQUEST") != 'true':
            return render(request, 'tracker/edit_workout_full.html', {'workout': workout, 'exercises': exercises_queryset})
        return render(request, 'tracker/edit_workout.html', {'workout': workout, 'exercises': exercises_queryset})

# PATCH used for saving exercisesets
    def patch(self, request, **kwargs):
        self.save_exercise_set(request, **kwargs)
        return HttpResponse(status=200, )

    def post(self, request, **kwargs):
        self.save_workout(request, **kwargs)
        return HttpResponse(status=200, headers={'HX-Redirect':'/workouts'})

    def save_workout(self, request, **kwargs):
        workout = WorkOut.objects.get(profile=request.user.profile, pk=kwargs['workout_pk'])
        workout.name = request.POST['name']
        workout.save()
        return

    def save_exercise_set(self, request, **kwargs):
        workout = WorkOut.objects.get(profile=request.user.profile, pk=kwargs['workout_pk'])
        try:
            exerciseset = ExerciseSet.objects.get(workout=workout, order_in_workout = int(request.POST['order_in_workout']))
        except:
            exerciseset = ExerciseSet(workout=workout, order_in_workout = int(request.POST['order_in_workout']))
        exerciseset.exercise = Exercise.objects.get(pk=int(request.POST['exercise']))
        
        exerciseset.to_failure = 'to_failure' in request.POST
        exerciseset.weight = int(request.POST['weight'])
        exerciseset.reps = int(request.POST['reps'])
        exerciseset.save()
    # guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # order_in_workout = models.IntegerField(null=False, blank=False, default=0) 
    # exercise = models.ForeignKey(Exercise, null=False, blank=False, on_delete=models.CASCADE)
    # workout = models.ForeignKey(WorkOut, null=False, blank=False, on_delete=models.CASCADE)
    # super_set_exercise_set = models.OneToOneField("ExerciseSet", null=True, default=None, on_delete=models.SET_NULL)
    # # performed = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    # to_failure = models.BooleanField(null=False, blank=False, default=False)
    # weight = models.IntegerField(null=False, blank=False, default=0) 
    # reps = models.IntegerField(null=False, blank=False, default=1) 
        return


def add_exercise_set(request, **kwargs):
    queryset = Exercise.objects.all()
    workout = WorkOut.objects.get(profile=request.user.profile, pk=kwargs['workout_pk'])
    return render(request, 'tracker/add_exercise_set.html', {'exercises': queryset, 'workout':workout, 'counter': kwargs['previous_counter']+1})
# def add_exercise_super_set(request, **kwargs):
#     queryset = Exercise.objects.all()
#     return render(request, 'tracker/add_exercise_super_set.html', {'exercises': queryset, 'counter': kwargs['counter']})

    # def post(self, request, *args, **kwargs):
    #     exercise = Exercise(name=request.POST['name'], alternative_names=request.POST['alternative_names'].split(','))
    #     exercise.save()
    #     try:
    #         for file in request.FILES.getlist('images'):
    #             image = ImageModel(image = file)
    #             image.save()
    #             exercise.images.add(image)
    #         exercise.save()
    #         return HttpResponseRedirect(self.success_url)
    #     except Exception as e:
    #         return HttpResponse(status=500)

# def add_exercise_super_set_button(request, **kwargs):
#     return render(request, 'tracker/exercise_super_set_button.html', {'counter':kwargs['counter']})
def send_email(subject, message, to=[]):
    msg = EmailMessage(subject,
                        message, to=to)
    msg.send()



def add_weigh_in(request, **kwargs):
    weighins = WorkOut.objects.filter(profile=request.user.profile)
    if request.META.get("HTTP_HX_REQUEST") != 'true':
        return render(request, 'tracker/weighins_full.html', {'weighins': weighins})
    return render(request, 'tracker/weighins.html', {'weighins': weighins})

class AddWeighinView(APIView):
    def get(self, request, **kwargs):
        weight_units = WEIGHT_UNIT_CHOICES
        if request.META.get("HTTP_HX_REQUEST") != 'true':
            return render(request, 'tracker/add_weighin.html', {'user': request.user, 'weight_units': weight_units})
        return render(request, 'tracker/add_weighin.html', {'user': request.user, 'weight_units': weight_units})
    def post(self, request, **kwargs):
        weight = convert_weight_to_grams(float(request.POST['weight_float']), request.POST['weight_unit_choice'])
        WeighIn.objects.get_or_create(profile=request.user.profile, weight=weight)
    
# class WeighIn(models.Model):
#     guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     profile = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE)
#     recorded = models.DateTimeField(auto_now_add=True, null=False, blank=False)
#     weight = models.FloatField(null=False, blank=False) 


        return HttpResponse(status=200, headers={'HX-Redirect':'/weighins'})

# WEIGHT_UNIT_CHOICES = (
#         ('a', 'kg'),
#         ('b', 'lb'),
#         ('c', 'stone'),
#     )
def convert_weight_to_grams(weight_float, weight_unit_choice):
    if weight_unit_choice == 'a':
        return weight_float * 1000
    elif weight_unit_choice == 'b':
        return weight_float / 0.0022046
    elif weight_unit_choice == 'c':
        return weight_float / 0.00015747

def convert_weight_from_grams_htmx_handler(request):
    print(request.GET['weight_float'])
    try:
        return HttpResponse(str(convert_weight_from_grams(float(request.GET['weight_float']), request.GET['weight_unit_choice'])))
    except:
        return HttpResponse("")
def convert_weight_from_grams(weight_float, weight_unit_choice):
    if weight_unit_choice == 'a':
        return "{} kg".format(str(round(weight_float / 1000, 1)))
    elif weight_unit_choice == 'b':
        return "{} lb".format(str(round(weight_float / 453.59237, 1)))
    elif weight_unit_choice == 'c':
        i, d = divmod(weight_float * 0.00015747, 1)
        return "{} stone {} lb".format(str(i), str(round(d/1.4, 1)))
        
    