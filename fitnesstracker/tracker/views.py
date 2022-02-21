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
        user = self.request.user
        return user.profile

    def get_success_url(self, *args, **kwargs):
        return reverse("index")

    def post(self, request, *args, **kwargs):
        profile, created = Profile.objects.get_or_create(user=request.user, fav_colour=request.POST['fav_colour'], weight_unit=request.POST['weight_unit'])
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
    queryset = Exercise.objects.filter(Q(name__icontains=request._post['search']) | Q(alternative_names__icontains=request._post['search']))
    # if request.META.get("HTTP_HX_REQUEST") != 'true':
    #     # return redirect('index')
    #     return render(request, 'tracker/exercise_catalogue_full.html', {'exercises': queryset})

    return render(request, 'tracker/exercise_catalogue_search_results.html', {'exercises': queryset})

def exercise_detail(request, **kwargs):
    exercise = Exercise.objects.get(pk=kwargs['pk'])
    if request.META.get("HTTP_HX_REQUEST") != 'true':
        return render(request, 'tracker/exercise_detail_full.html', {'exercise': exercise})
    return render(request, 'tracker/exercise_detail.html', {'exercise': exercise})
