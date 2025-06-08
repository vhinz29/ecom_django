from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control' ,'placeholder': 'Email Address'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control' ,'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50 ,widget=forms.TextInput(attrs={'class':'form-control' ,'placeholder': 'Last Name'}))


    class Meta:
        model = User
        fields = ('username' ,'first_name', 'last_name', 'email' ,'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(SignUpForm ,self).__init__(*args ,**kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'




class ProfileForm(ModelForm):
    class Meta:
        model = Profile

        # fields = "__all__"
        fields = ('user', 'todaname', 'zone', 'first_name' , 'last_name','phone' ,'email' , 'bodynum','license_id','license_expired', 'image')

        labels = {
            'user': '',
            'todaname': '',
            'zone': '',
            'first_name': '',
            'last_name': '',
            'phone': '',
            'email': '',
            'bodynum': '',
            'license_id': '',
            'license_expired':'',
            'image': '',
        }

        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'  ,'placeholder': 'Username'}),
            'todaname': forms.Select(attrs={'class': 'form-select' ,'placeholder': 'Todaname'}),
            'zone': forms.Select(attrs={'class': 'form-select' ,'placeholder': 'Zonename'}),
      'first_name': forms.TextInput(attrs={'class': 'form-control' ,'placeholder': 'First Name'}),
       'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
           'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
           'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
         'bodynum': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Body Number'}),
            'license_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'License ID'}),
            'license_expired': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'License Expired'}),
            # 'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Image'}),

        }

class ProfileRegistrationForm(forms.ModelForm):
	# user = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-select', 'placeholder':'Username'}), required=True)
	# zone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-select', 'placeholder':'Zonename'}), required=True)
    first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=True)
    last_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=True)
    phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}), required=True)
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=True)
    bodynum = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Body Number'}), required=False)
    license_id = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'License ID'}),required=True)
    license_expired = forms.DateField(label="",widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'License Expired'}),required=False)



    class Meta:
        model = Profile
        fields = ('user', 'todaname', 'zone', 'first_name' , 'last_name','phone' ,'email' , 'bodynum','license_id','license_expired', 'image')
