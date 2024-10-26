from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Post
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            try:
                user = User.objects.get(username=username)
                if not user.check_password(password):
                    raise forms.ValidationError("Invalid password")
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid username")

        return cleaned_data

    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

# 2nd Flaw.: No password strength validation
# Fix: Add validation in the form:

# from django.core.exceptions import ValidationError
# def validate_password(value):
#    if len(value) < 8:  # Minimum length
#        raise ValidationError('Password must be at least 8 characters long.')
#    if not any(char.isdigit() for char in value):  # At least one digit
#        raise ValidationError('Password must contain at least one digit.')

#class RegistrationForm(forms.ModelForm):
#    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
