import json

from django.db import transaction
from django.db.models import F, Q
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import FormView, ListView
from django.views.generic.detail import BaseDetailView, DetailView

from order.forms import SubmitOrderForm
from order.models import Order, OrderStatus
from order.serializer import OrderDetailSerializer, OrderListSerializer
from utils.response import FormValidationFailJsonResponse, NotFoundJsonResponse
from utils.views import login_require


@method_decorator(login_require, name='dispatch')
class TicketOrderSubmitView(FormView):
    http_method_names = ['post']
    form_class = SubmitOrderForm

    def form_invalid(self, form):
        err = json.loads(form.errors.as_json())
        return FormValidationFailJsonResponse(err)

    def form_valid(self, form):
        order_obj = form.save(user=self.request.user)
        return JsonResponse({
            'sn': order_obj.sn
        }, status=201)


# add the decorator "login_require" to the method dispatch.
# method dispatch will call method get , post accordingly
@method_decorator(login_require, name='dispatch')
class OrderDetail(BaseDetailView):
    # unlike other detail view, this one get the object not by pk , but order number
    # slug_field and slug_url_kwarg needed to be specified
    slug_field = 'sn'
    slug_url_kwarg = 'sn'

    def get_queryset(self):
        return Order.objects.filter(is_valid=True, user=self.request.user)

    # RESTful API - GET - require the detail of the order
    def get(self, request, *args, **kwargs):
        # get_object: get object based on order number, if no object of found, return 404
        order_obj = self.get_object()
        data = OrderDetailSerializer(order_obj).to_dict()
        return JsonResponse(data)

    # multiple tables are updated, transaction is needed to asure the Atomicity
    @transaction.atomic
    # RESTful API - POST - pay the order
    def post(self, request, *args, **kwargs):
        order_obj = self.get_object()
        if order_obj.status == OrderStatus.SUBMIT:
            # TODO call the real payment method
            order_obj.status = OrderStatus.PAID
            order_obj.save()
            order_obj.order_items.update(status=OrderStatus.PAID)
            return HttpResponse('', status=201)
        return HttpResponse('', status=200)

    # RESTful API - DELETE - delete the order
    def delete(self, request, *args, **kwargs):
        order_obj = self.get_object()
        if order_obj.status == OrderStatus.CANCELED or order_obj.status == OrderStatus.PAID:
            order_obj.is_valid = False
            order_obj.save()
            return HttpResponse("", status=201)
        else:
            return HttpResponse("", status=200)

    # multiple tables are updated, transaction is needed to asure the Atomicity
    @transaction.atomic
    # RESTful API - PUT - cancel the order
    def put(self, request, *args, **kwargs):
        order_obj = self.get_object()
        if order_obj.status == OrderStatus.SUBMIT:
            order_obj.status = OrderStatus.CANCELED
            order_obj.save()
            order_items_list = order_obj.order_items.filter(status=OrderStatus.SUBMIT)
            for order_items_obj in order_items_list:
                ticket_obj = order_items_obj.ticket
                ticket_obj.stock = F('stock') + order_items_obj.count
                ticket_obj.save()
            order_items_list.update(status=OrderStatus.CANCELED)
            return HttpResponse('', status=201)
        return HttpResponse('', status=200)


@method_decorator(ensure_csrf_cookie, name='dispatch')
@method_decorator(login_require, name='dispatch')
class OrderListView(ListView):
    # show 10 records per page
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        query = Q(is_valid=True, user=user)
        order_status = self.request.GET.get('status', None)
        if order_status and order_status != '0':
            query = query & Q(status=order_status)

        return Order.objects.filter(query).order_by('-update_at')

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['page_obj']
        if page_obj is not None:
            data = OrderListSerializer(page_obj).to_dict()
            return JsonResponse(data)
        else:
            return NotFoundJsonResponse()

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('limit', None)
        return paginate_by or self.paginate_by



