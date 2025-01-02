from django.contrib import admin
from .models import User, Events, RSVP

# Register your models here.
admin.site.register(User)
admin.site.register(Events)
admin.site.register(RSVP)
