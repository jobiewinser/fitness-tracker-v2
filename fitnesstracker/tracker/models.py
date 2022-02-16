from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    def get_or_create_profile(self):
        try:
            profile, created = Profile.objects.get_or_create(user = self)
        except Exception as e:
            pass
        return profile

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='profile', on_delete=models.CASCADE)
    fav_colour = models.CharField(blank=True, null=True, max_length=120)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.fav_colour = 'black'
        super(Profile, self).save(*args, **kwargs)

class WorkOut(models.Model):
    pass

class Exercise(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    alternative_names = ArrayField(
        models.CharField(max_length=50, blank=True, null=True),
        null=True,
        blank=True
    )
    # completed = models.BooleanField(default=False)

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