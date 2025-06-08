from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from information.models import Addinfo, Seminars


class SeminarsRegistrationForm(ModelForm):
    # id_driver = forms.Select(label="", widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Username'}), required=True)
    seminar_dates = forms.CharField(label="",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seminar Dates'}),
                                required=False)


    class Meta:
        model = Seminars
        fields = ('id_driver', 'seminar_dates')


class AddinfoRegistrationForm(ModelForm):

    # user_addinfo = forms.Select(label="", widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Username'}), required=True)
    ID_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'ID Number'}), required=True)
    ID_issue = forms.DateField(label="", widget=forms.DateInput(attrs={'class':'form-control', 'placeholder':'ID Issue'}), required=True)
    ID_expired = forms.DateField(label="", widget=forms.DateInput(attrs={'class':'form-control', 'placeholder':'ID Expired'}), required=True)


    class Meta:
        model = Addinfo
        fields = ('user_addinfo', 'ID_number', 'ID_issue', 'ID_expired')




class AddinfoForm(ModelForm):
    class Meta:
        model = Addinfo

        fields = ('user_addinfo' ,'ID_number', 'ID_issue', 'ID_expired')

        labels = {
            'user_addinfo': 'Username',
            'ID_number': 'ID Number',
            'ID_issue': 'ID Issue',
            'ID_expired': 'ID Expired',

        }

        widgets = {

      'user_addinfo': forms.Select(attrs={'class': 'form-select' ,'placeholder': 'Username'}),
       'ID_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID Number'}),
       'ID_issue': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'ID Issue'}),
       'ID_expired': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'ID Expired'}),

        }


class SeminarsForm(ModelForm):
    class Meta:
        model = Seminars

        fields = ('id_driver', 'seminar_dates')

        labels = {
            'id_driver': 'ID Number',
            'seminar_dates': 'Seminar Date',

        }

        widgets = {

            'id_driver': forms.Select(attrs={'class': 'form-select', 'placeholder': 'ID Driver'}),
            'seminar_dates': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Seminars Date'}),

        }


# class AttendanceForm(ModelForm):
#     class Meta:
#         model = Attendance
#
#         # fields = "__all__"
#         fields = ('user_attend', 'log_in', 'log_out', 'total_hour' , 'total_rate' ,'total_salary')
#
#         labels = {
#             'user_attend': '',
#             'log_in': '',
#             'log_out': '',
#             'total_hour': '',
#             'total_rate': '',
#             'total_salary': '',
#
#         }
#
#         widgets = {
#
#       'user_attend': forms.TextInput(attrs={'class': 'form-control' ,'placeholder': 'User Attend'}),
#        'log_in': forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Log-in'}),
#            'log_out': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Log-out'}),
#            'total_hour': forms.DecimalField(attrs={'class': 'form-control', 'placeholder': 'Total Hour'}),
#          'total_rate': forms.DecimalField(attrs={'class': 'form-control', 'placeholder': 'Total Rate'}),
#             'total_salary': forms.DecimalField(attrs={'class': 'form-control', 'placeholder': 'Total Salary'}),
#
#         }
#
#
# class Febs_2025Form(ModelForm):
#     class Meta:
#         model = Febs_2025
#
#         # fields = "__all__"
#         fields = ('user_attend', 'log_in', 'log_out', 'total_hour' , 'total_rate' ,'total_salary')
#
#         labels = {
#             'user_attend': '',
#             'log_in': '',
#             'log_out': '',
#             'total_hour': '',
#             'total_rate': '',
#             'total_salary': '',
#
#         }
#
#         widgets = {
#
#       'user_attend': forms.TextInput(attrs={'class': 'form-control' ,'placeholder': 'User Attend'}),
#        'log_in': forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Log-in'}),
#            'log_out': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Log-out'}),
#            'total_hour': forms.DecimalField(attrs={'class': 'form-control', 'placeholder': 'Total Hour'}),
#          'total_rate': forms.DecimalField(attrs={'class': 'form-control', 'placeholder': 'Total Rate'}),
#             'total_salary': forms.DecimalField(attrs={'class': 'form-control', 'placeholder': 'Total Salary'}),
#
#         }
#
# class Febs_2025Form(ModelForm):
#     class Meta:
#         model = Aprs_2025
#
#         # fields = "__all__"
#         fields = ('user_attend', 'log_in', 'log_out', 'total_hour' , 'total_rate' ,'total_salary')
#
#         labels = {
#             'user_attend': '',
#             'log_in': '',
#             'log_out': '',
#             'total_hour': '',
#             'total_rate': '',
#             'total_salary': '',
#
#         }
#
#         widgets = {
#
#       'user_attend': forms.TextInput(attrs={'class': 'form-control' ,'placeholder': 'User Attend'}),
#        'log_in': forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Log-in'}),
#            'log_out': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Log-out'}),
#            'total_hour': forms.DecimalField(attrs={'class': 'form-control', 'placeholder': 'Total Hour'}),
#          'total_rate': forms.DecimalField(attrs={'class': 'form-control', 'placeholder': 'Total Rate'}),
#             'total_salary': forms.DecimalField(attrs={'class': 'form-control', 'placeholder': 'Total Salary'}),
#
#         }
#
#
