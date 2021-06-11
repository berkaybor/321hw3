from django import forms

class LoginForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    institution = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Institution'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Password'}))