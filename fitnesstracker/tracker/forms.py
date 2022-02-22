from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Profile, Exercise
from django.forms import ModelForm
from django.contrib.postgres.forms import SimpleArrayField
from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name']

class UserLoginForm(AuthenticationForm):
    # email = forms.EmailField()

    class Meta:
        model = CustomUser
        # fields = ['email']

class ProfileForm(ModelForm):
    pictures = forms.FileField(label='Select a file to upload', widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    class Meta:
        model = Profile
        fields = ['fav_colour', 'display_name', 'weight_unit', 'pictures']

class ExerciseCreateForm(ModelForm):
    alternative_names = SimpleArrayField(forms.CharField(max_length=100), delimiter=',')
    # images = MultiImageField(min_num=1, max_num=20)
    images = forms.FileField(label='Select a file to upload', widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    class Meta:
        model = Exercise
        # fields = ['name']
        fields = ['name', 'alternative_names', 'images']
        