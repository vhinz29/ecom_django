from django.contrib import admin
from .models import Zone, Profile, Logo, Todaname, Notifies
from django.contrib.auth.models import User

admin.site.register(Logo)
admin.site.register(Zone)
# admin.site.register(Notifies)



@admin.register(Notifies)
class NotifiesAdmin(admin.ModelAdmin):
    list_display = ('notify_user','is_seen')
    ordering = ('notify_user',)
    search_fields = ('notify_user','is_seen')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','first_name', 'last_name','email','bodynum','zone')
    ordering = ('zone','last_name')
    search_fields = ('first_name','last_name','bodynum')


@admin.register(Todaname)
class TodanameAdmin(admin.ModelAdmin):
    list_display = ('name_toda', 'brgy_name','todazone')
    ordering = ('todazone','brgy_name')
    search_fields = ('brgy_name' ,'name_toda')