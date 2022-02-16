from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.views.generic.edit import CreateView
from .forms import UserRegisterForm, UserLoginForm

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

def index(request):
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