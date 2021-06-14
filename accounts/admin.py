from django.contrib import admin
from .models import Profile

@admin.register(Profile) #데코레이터. == admin.site.register()
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['email', 'nickname', 'date_joined']
    list_display_links = ['email', 'nickname']

