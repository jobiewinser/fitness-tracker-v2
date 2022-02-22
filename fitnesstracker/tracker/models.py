from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
import hashlib
import random
import uuid

class CustomUser(AbstractUser):
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    def get_or_create_profile(self):
        try:
            profile, created = Profile.objects.get_or_create(user = self)
            print(profile)
        except Exception as e:
            pass
        return profile

    def save(self, *args, **kwargs):
        return super(CustomUser, self).save(*args, **kwargs)

class ImageModel(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to="uploads/exercises")
    uploaded_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    class Meta:
        get_latest_by = 'uploaded_date'

    def save(self, *args, **kwargs):
        return super(ImageModel, self).save(*args, **kwargs)

class Profile(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(CustomUser, related_name='profile', on_delete=models.CASCADE)
    display_name = models.CharField(max_length=20, blank=False, null=False, unique=True)
    pictures = models.ManyToManyField(ImageModel)
    COLOUR_CHOICES = (
        ('a', 'Black'),
        ('b', 'DarkBlue'),
        ('c', 'DarkSlateGray'),
    )
    fav_colour = models.CharField(max_length=20, default="a", choices=COLOUR_CHOICES)
    
    WEIGHT_UNIT_CHOICES = (
        ('a', 'kg'),
        ('b', 'lb'),
        ('c', 'stone'),
    )
    weight_unit = models.CharField(max_length=20, default="a", choices=WEIGHT_UNIT_CHOICES)
    def save(self, *args, **kwargs):
        return super(Profile, self).save(*args, **kwargs)

class WorkOut(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    profile = models.ForeignKey(Profile, related_name='workouts', on_delete=models.CASCADE) 
    name = models.CharField(max_length=50, null=False, blank=False)
    def save(self, *args, **kwargs):
        return super(WorkOut, self).save(*args, **kwargs)

class Exercise(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    archived = models.BooleanField(null=False, blank=False, default=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    alternative_names = ArrayField(
        models.CharField(max_length=50, blank=True, null=True),
        null=True,
        blank=True
    )
    images = models.ManyToManyField(ImageModel)
    def save(self, *args, **kwargs):
        return super(Exercise, self).save(*args, **kwargs)
    
class ExerciseSet(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    exercise = models.ForeignKey(Exercise, null=False, blank=False, on_delete=models.CASCADE)
    work_out = models.ForeignKey(WorkOut, null=False, blank=False, on_delete=models.CASCADE)
    super_set_exercise_set = models.OneToOneField("ExerciseSet", null=True, default=None, on_delete=models.SET_NULL)
    # performed = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    to_failure = models.BooleanField(null=False, blank=False, default=False)
    weight = models.IntegerField(null=False, blank=False, default=0) 
    reps = models.IntegerField(null=False, blank=False, default=1) 
    
# class ExerciseSubSet(models.Model):
#     guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     exercise_set = models.ForeignKey(ExerciseSet, null=False, blank=False, on_delete=models.CASCADE)
    
class WeighIn(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    profile = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE)
    recorded = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    weight = models.FloatField(null=False, blank=False) 