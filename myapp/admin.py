from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User, Event, EventsJoined

admin.site.register(User)
admin.site.register(Event)
admin.site.register(EventsJoined)