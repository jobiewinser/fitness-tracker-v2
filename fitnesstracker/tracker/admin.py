from django.contrib import admin
from django.apps import apps
# Register your models here.
models = apps.get_models()

model_register_blacklist = ['']

for model in models:
    try:
        if model.__name__ not in model_register_blacklist:
            admin.site.register(model)
        else:
            print("skipped registering "+str(model.__name__))
    except admin.sites.AlreadyRegistered:
        pass
