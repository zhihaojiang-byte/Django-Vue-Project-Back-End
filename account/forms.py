import re

from django import forms
from django.contrib.auth import authenticate, login
from django.core.cache import cache

from account.models import User

password_format = {"pattern": r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,30}$",
                   "message": "Password should be 6~30 long, contains at least one letter, one number and one special character"}
username_format = {"pattern": r"^[A-Za-z0-9_]{6,30}$",
                   "message": "Username should be 6~30 long and only contain letters, numbers or underscores"}
verification_code_format = {"pattern": r"^[0-9]{4}$",
                            "message": "Verification code should be 4 digits"}


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={
        'required': "E-mail address is required",
    })
    password = forms.CharField(required=True, error_messages={
        'required': "Password is required",
    })

    user = None

    def clean(self):
        data = super().clean()
        if self.errors:
            return
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(username=email, password=password)
        if user is None:
            raise forms.ValidationError("The email or password is incorrect.")
        elif not user.is_active:
            raise forms.ValidationError("The account has been frozen.")
        self.user = user
        return data

    def user_login(self, request):
        login(request, self.user)
        return self.user


class RegisterForm(forms.Form):
    username = forms.CharField(required=True, label='username', error_messages={
        'required': "Username is required",
    })
    password = forms.CharField(required=True, label='password', error_messages={
        'required': "Password is required",
    })
    email = forms.EmailField(required=True, error_messages={
        'required': "E-mail address is required",
    })
    verification_code = forms.CharField(
        required=True, label='verification_code', error_messages={
            'required': "Verification code is required"
        })

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(username_format['pattern'], username):
            raise forms.ValidationError(username_format['message'])
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if not re.search(password_format['pattern'], password):
            raise forms.ValidationError(password_format['message'])
        return password

    def clean_verification_code(self):
        verification_code = self.cleaned_data['verification_code']
        if not re.search(verification_code_format['pattern'], verification_code):
            raise forms.ValidationError(verification_code_format['message'])
        return verification_code

    def clean(self):
        data = super().clean()
        if self.errors:
            return
        email = data.get('email', None)
        verification_code = data.get('verification_code', None)

        verification_code_cache = cache.get(email)
        if verification_code_cache is None:
            raise forms.ValidationError("Verification code is not correct")
        if str(verification_code_cache) != verification_code:
            raise forms.ValidationError("Verification code is not correct")
        return data

    def user_register(self, request):
        try:
            data = self.cleaned_data
            user = User.objects.create_user(
                username=data.get('username', None),
                password=data.get('password', None),
                email=data.get('email', None),
            )
            user.save()
            login(request, user)
            return user
        except Exception as e:
            print(e)
            return None



