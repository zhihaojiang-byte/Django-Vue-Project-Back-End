import json

from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView

from account.forms import LoginForm, RegisterForm
from account.serializer import UserSerializer
from utils.response import FormValidationFailJsonResponse, MethodNotAllowedJsonResponse, UnauthorizedJsonResponse, \
    ServerErrorJsonResponse

from django.views.decorators.csrf import ensure_csrf_cookie


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.user_login(request)
            data = UserSerializer(user).to_dict()
            return JsonResponse(data)
        else:
            errors = json.loads(form.errors.as_json())
            return FormValidationFailJsonResponse(error_list=errors)
    else:
        return MethodNotAllowedJsonResponse()


def user_logout(request):
    logout(request)
    return HttpResponse(status=201)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserInfo(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            data = UserSerializer(user).to_dict()
            return JsonResponse(data)
        else:
            return UnauthorizedJsonResponse()


class UserRegister(FormView):
    form_class = RegisterForm
    http_method_names = ['post']

    def form_valid(self, form):
        user = form.user_register(request=self.request)
        if user is not None:
            data = UserSerializer(user).to_dict()
            return JsonResponse(data)
        return ServerErrorJsonResponse()

    def form_invalid(self, form):
        error_list = json.loads(form.errors.as_json())
        return FormValidationFailJsonResponse(error_list=error_list)
