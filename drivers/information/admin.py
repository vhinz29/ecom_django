from django.contrib import admin
from .models import Addinfo,Seminars, Attendance,Febs_2025 ,Aprs_2025
from .models import Jans_2025, Mays_2025, Junes_2025, Julys_2025
from .models import Augs_2025, Septs_2025, Octs_2025, Novs_2025, Decs_2025
from django.contrib.auth.models import User

# admin.site.register(Addinfo)
# admin.site.register(Seminars)
# admin.site.register(Attendance)
# admin.site.register(Febs_2025)
# admin.site.register(Aprs_2025)


@admin.register(Addinfo)
class AddinfoAdmin(admin.ModelAdmin):
    list_display = ('user_addinfo','ID_number', 'ID_issue','ID_expired')
    ordering = ('user_addinfo','ID_number')
    search_fields = ('ID_number',)


@admin.register(Seminars)
class SeminarsAdmin(admin.ModelAdmin):
    list_display = ('id_driver','seminar_dates')
    ordering = ('id_driver','seminar_dates')
    search_fields = ('seminar_dates',)


@admin.register(Attendance)
# admin.site.register(Febs_2025)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user_attend' ,'log_in', 'log_out' ,'total_hour' ,'total_rate' ,'total_salary',
                    'ot_request', 'ot_request_time','ot_approved','ot_approved_time')
    ordering = ('log_in','user_attend')
    search_fields = ('user_attend', 'log_in')


@admin.register(Febs_2025)
class Febs_2025Admin(admin.ModelAdmin):
    list_display = ('user_attend', 'log_in', 'log_out', 'total_hour', 'total_rate', 'total_salary',
                    'ot_request', 'ot_request_time', 'ot_approved', 'ot_approved_time')
    ordering = ('log_in', 'user_attend')
    search_fields = ('user_attend', 'log_in')

@admin.register(Aprs_2025)
class Aprs_2025Admin(admin.ModelAdmin):
    list_display = ('user_attend', 'log_in', 'log_out', 'total_hour', 'total_rate', 'total_salary',
                    'ot_request', 'ot_request_time', 'ot_approved', 'ot_approved_time')

    ordering = ('log_in', 'user_attend')
    search_fields = ('user_attend', 'log_in')

@admin.register(Jans_2025)
class Jans_2025Admin(admin.ModelAdmin):

    list_display = ('user_attend', 'log_in', 'log_out', 'total_hour', 'total_rate', 'total_salary',
                    'ot_request', 'ot_request_time', 'ot_approved', 'ot_approved_time' , 'decoy_vars')
    # exclude = ('decoy_vars',)
    ordering = ('log_in', 'user_attend')
    search_fields = ('user_attend', 'log_in')



@admin.register(Mays_2025)
class Mays_2025Admin(admin.ModelAdmin):
    list_display = ('user_attend', 'log_in', 'log_out', 'total_hour', 'total_rate', 'total_salary',
                    'ot_request', 'ot_request_time', 'ot_approved', 'ot_approved_time')
    ordering = ('log_in', 'user_attend')
    search_fields = ('user_attend', 'log_in')

@admin.register(Junes_2025)
class Junes_2025Admin(admin.ModelAdmin):
    list_display = ('user_attend', 'log_in', 'log_out', 'total_hour', 'total_rate', 'total_salary',
                    'ot_request', 'ot_request_time', 'ot_approved', 'ot_approved_time')
    ordering = ('log_in', 'user_attend')
    search_fields = ('user_attend', 'log_in')

@admin.register(Julys_2025)
class Julys_2025Admin(admin.ModelAdmin):
    list_display = ('user_attend', 'log_in', 'log_out', 'total_hour', 'total_rate', 'total_salary',
                    'ot_request', 'ot_request_time', 'ot_approved', 'ot_approved_time')
    ordering = ('log_in', 'user_attend')
    search_fields = ('user_attend', 'log_in')

@admin.register(Augs_2025)
class Augs_2025Admin(admin.ModelAdmin):
    list_display = ('user_attend', 'log_in', 'log_out', 'total_hour', 'total_rate', 'total_salary',
                    'ot_request', 'ot_request_time', 'ot_approved', 'ot_approved_time')
    ordering = ('log_in', 'user_attend')
    search_fields = ('user_attend', 'log_in')

@admin.register(Septs_2025)
class Septs_2025Admin(admin.ModelAdmin):
    list_display = ('user_attend', 'log_in', 'log_out', 'total_hour', 'total_rate', 'total_salary',
                    'ot_request', 'ot_request_time', 'ot_approved', 'ot_approved_time')
    ordering = ('log_in', 'user_attend')
    search_fields = ('user_attend', 'log_in')

@admin.register(Octs_2025)
class Octs_2025Admin(admin.ModelAdmin):
    list_display = ('user_attend', 'log_in', 'log_out', 'total_hour', 'total_rate', 'total_salary',
                    'ot_request', 'ot_request_time', 'ot_approved', 'ot_approved_time')
    ordering = ('log_in', 'user_attend')
    search_fields = ('user_attend', 'log_in')

@admin.register(Novs_2025)
class Novs_2025Admin(admin.ModelAdmin):
    list_display = ('user_attend', 'log_in', 'log_out', 'total_hour', 'total_rate', 'total_salary',
                    'ot_request', 'ot_request_time', 'ot_approved', 'ot_approved_time')
    ordering = ('log_in', 'user_attend')
    search_fields = ('user_attend', 'log_in')

@admin.register(Decs_2025)
class Decs_2025Admin(admin.ModelAdmin):
    list_display = ('user_attend', 'log_in', 'log_out', 'total_hour', 'total_rate', 'total_salary',
                    'ot_request', 'ot_request_time', 'ot_approved', 'ot_approved_time')
    ordering = ('log_in', 'user_attend')
    search_fields = ('user_attend', 'log_in')


