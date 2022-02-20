from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    def get_or_create_profile(self):
        try:
            profile, created = Profile.objects.get_or_create(user = self)
            print(profile)
        except Exception as e:
            pass
        return profile

    def save(self, *args, **kwargs):
        return super(CustomUser, self).save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='profile', on_delete=models.CASCADE)

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
    pass

class ImageModel(models.Model):
    image = models.ImageField(upload_to="uploads/exercises")
    def save(self, *args, **kwargs):
        return super(ImageModel, self).save(*args, **kwargs)


class Exercise(models.Model):
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
    profile = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, null=False, blank=False, on_delete=models.CASCADE)
    work_out = models.ForeignKey(WorkOut, null=False, blank=False, on_delete=models.CASCADE)
    super_set_exercise_set = models.OneToOneField("ExerciseSet", null=True, default=None, on_delete=models.SET_NULL)
    performed = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    
class ExerciseSubSet(models.Model):
    exercise_set = models.ForeignKey(ExerciseSet, null=False, blank=False, on_delete=models.CASCADE)
    to_failure = models.BooleanField(null=False, blank=False, default=False)
    
class WeighIn(models.Model):
    profile = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE)
    recorded = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    weight = models.FloatField(null=False, blank=False) 