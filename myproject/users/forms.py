from django import forms
from .models import User, UploadedFile

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'mobile']

class LoginForm(forms.Form):
    mobile = forms.CharField(max_length=10)
    otp = forms.CharField(max_length=4)

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
