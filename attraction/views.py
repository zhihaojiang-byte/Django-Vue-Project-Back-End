import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView, DetailView, FormView
from django.db.models import Q

from attraction.forms import PostCommentForm
from attraction.models import Attraction, AttractionInfo, Ticket, TicketInfo
from django.http import JsonResponse

from attraction.serializer import AttractionListPageSerializer, AttractionDetailSerializer, \
    CommentListPageSerializer, TicketListPageSerializer, AttractionInfoSerializer, TicketSerializer, \
    TicketInfoSerializer, AttractionImagesPageSerializer
from utils.response import NotFoundJsonResponse, FormValidationFailJsonResponse
from utils.views import login_require


class AttractionList(ListView):
    """get attractions list by page"""
    # setting items count per page
    paginate_by = 5

    def get_queryset(self):
        query = Q(is_valid=True)

        is_popular = self.request.GET.get('is_popular', None)
        if is_popular:
            query = query & Q(is_popular=True)

        is_recommended = self.request.GET.get('is_recommended', None)
        if is_recommended:
            query = query & Q(is_recommended=True)

        keyword = self.request.GET.get('keyword', None)
        if keyword:
            query = query & Q(name__icontains=keyword)

        query_set = Attraction.objects.filter(query)
        return query_set

    def get_paginate_by(self, queryset):
        page_size = self.request.GET.get('limit', None)
        return page_size or self.paginate_by

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['page_obj']
        if page_obj is not None:
            data = AttractionListPageSerializer(page_obj).to_dict()
            return JsonResponse(data)
        else:
            return NotFoundJsonResponse()


class AttractionDetail(DetailView):
    def get_queryset(self):
        return Attraction.objects.all()

    def render_to_response(self, context, **response_kwargs):

        obj = context['object']

        if obj is not None and obj.is_valid is True:
            data = AttractionDetailSerializer(obj).to_dict()
            return JsonResponse(data)
        else:
            return NotFoundJsonResponse()


class AttractionImages(ListView):
    paginate_by = 5

    def get_queryset(self):
        attraction_id = self.kwargs.get('pk', None)
        attraction = Attraction.objects.filter(id=attraction_id, is_valid=True).first()
        if attraction:
            return attraction.images.filter(is_valid=True).order_by('-update_at')

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['page_obj']
        if page_obj is not None:
            data = AttractionImagesPageSerializer(page_obj).to_dict()
            return JsonResponse(data)
        else:
            return NotFoundJsonResponse()


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CommentList(ListView):
    paginate_by = 10

    def get_queryset(self):
        attraction_id = self.kwargs.get('pk', None)
        attraction = Attraction.objects.filter(id=attraction_id, is_valid=True).first()
        if attraction:
            return attraction.comments.filter(is_valid=True)

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['page_obj']
        if page_obj is not None:
            data = CommentListPageSerializer(page_obj).to_dict()
            return JsonResponse(data)
        else:
            return NotFoundJsonResponse()


class TicketList(ListView):
    paginate_by = 100

    def get_queryset(self):
        attraction_id = self.kwargs.get('pk', None)
        attraction = Attraction.objects.filter(id=attraction_id, is_valid=True).first()
        if attraction:
            return attraction.tickets.filter(is_valid=True).order_by('order')

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['page_obj']
        if page_obj is not None:
            data = TicketListPageSerializer(page_obj).to_dict()
            return JsonResponse(data)
        else:
            return NotFoundJsonResponse()


class AttractionInfoView(DetailView):
    pk_url_kwarg = None
    slug_url_kwarg = 'pk'
    slug_field = 'attraction__pk'

    def get_queryset(self):
        return AttractionInfo.objects.all()

    def render_to_response(self, context, **response_kwargs):

        obj = context['object']

        if obj is not None and obj.is_valid is True:
            data = AttractionInfoSerializer(obj).to_dict()
            return JsonResponse(data)
        else:
            return NotFoundJsonResponse()


class TicketDetailView(DetailView):
    def get_queryset(self):
        return Ticket.objects.filter(is_valid=True)

    def render_to_response(self, context, **response_kwargs):

        obj = context['object']

        if obj is not None and obj.is_valid is True:
            data = TicketSerializer(obj).to_dict()
            return JsonResponse(data)
        else:
            return NotFoundJsonResponse()


class TicketInfoView(DetailView):
    pk_url_kwarg = None
    slug_url_kwarg = 'pk'
    slug_field = 'ticket__pk'

    def get_queryset(self):
        return TicketInfo.objects.all()

    def render_to_response(self, context, **response_kwargs):

        obj = context['object']

        if obj is not None and obj.is_valid is True:
            data = TicketInfoSerializer(obj).to_dict()
            return JsonResponse(data)
        else:
            return NotFoundJsonResponse()


@method_decorator(login_require, name='dispatch')
class PostCommentView(FormView):
    http_method_names = ['post']
    form_class = PostCommentForm

    def form_invalid(self, form):
        err = json.loads(form.errors.as_json())
        return FormValidationFailJsonResponse(err)

    def form_valid(self, form):
        form.save(user=self.request.user)
        return JsonResponse({
        }, status=201)
