import json

from django.core.cache import cache
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import FormView

from system.forms import VerificationCodeForm
from system.models import Swipe
from utils.response import ServerErrorJsonResponse, FormValidationFailJsonResponse


@ensure_csrf_cookie
def slider_list(request):
    data = {
        'meta': {

        },
        'object': [],
    }
    query_set = Swipe.objects.filter(is_valid=True).order_by('order')

    for item in query_set:
        data['object'].append(
            {
                'id': item.id,
                'name': item.name,
                'img_url': item.img.url,
                'target_url': item.target_url,
            }
        )

    return JsonResponse(data)


class SendVerificationCode(FormView):
    form_class = VerificationCodeForm
    http_method_names = ['post']

    def form_valid(self, form):
        data = form.send_verification_code()
        if data is not None:
            return JsonResponse(data)
        return ServerErrorJsonResponse()

    def form_invalid(self, form):
        error_list = json.loads(form.errors.as_json())
        return FormValidationFailJsonResponse(error_list=error_list)


def cache_set(request):
    cache.set('username', 'lis')
    return HttpResponse('ok')


def cache_get(request):
    name = cache.get('username')
    return HttpResponse(name)

 
