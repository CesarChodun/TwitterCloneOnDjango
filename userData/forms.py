from django import forms

class RegisterNewUser(forms.Form):
    login = forms.CharField(label="Login", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, max_length=25)
    email = forms.EmailField()

class LoginUser(forms.Form):
    login = forms.CharField(label="Login", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, max_length=25)
