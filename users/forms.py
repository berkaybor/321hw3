from django import forms

class UserLoginForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    institution = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Institution'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class DBManagerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class UserAddForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    institution = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Institution'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))