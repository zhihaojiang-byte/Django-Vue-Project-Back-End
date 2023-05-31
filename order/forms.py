from django import forms
from django.db import transaction
from django.db.models import F

from attraction.models import Ticket
from order.models import Order, OrderItem
from utils import tools


class SubmitOrderForm(forms.ModelForm):
    ticket_id = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ticket_obj = None

    class Meta:
        model = Order
        fields = ('full_name', 'purchase_count')

    def clean_ticket_id(self):
        ticket_id = self.cleaned_data['ticket_id']
        self.ticket_obj = Ticket.objects.filter(is_valid=True, pk=ticket_id).first()
        if self.ticket_obj is None:
            raise forms.ValidationError('Ticket is not valid')
        elif self.ticket_obj.stock <= 0:
            raise forms.ValidationError('Ticket is sold out.')
        return ticket_id

    def clean(self):
        if self.errors:
            return
        cleaned_data = super().clean()
        purchase_count = cleaned_data.get("purchase_count")

        if self.ticket_obj.stock - purchase_count < 0:
            raise forms.ValidationError('Insufficient tickets. Please reduce the purchase count.')

        return cleaned_data

    # multiple tables are updated, transaction is needed to asure the Atomicity
    @transaction.atomic
    # manually save the object to database , commit=False
    def save(self, user, commit=False):
        # create an order_obj, assign the other fields and save
        order_obj = super().save(commit=commit)
        order_obj.user = user
        order_obj.sn = tools.gen_trans_id()
        purchase_count = self.cleaned_data['purchase_count']
        # purchase_amount should not be acquired from the frond end
        purchase_amount = self.ticket_obj.sell_price * purchase_count
        order_obj.purchase_amount = purchase_amount
        order_obj.save()

        # update the ticket stock and save
        # F function: update the data in database level, not in python level
        self.ticket_obj.stock = F('stock') - purchase_count
        self.ticket_obj.save()

        # create an orderItem, assign the fields and save
        OrderItem.objects.create(
            user=user,
            order=order_obj,
            flash_name=self.ticket_obj.name,
            flash_image=self.ticket_obj.attraction.cover_img,
            flash_price=self.ticket_obj.price,
            flash_discount=self.ticket_obj.discount,
            flash_sell_price=self.ticket_obj.sell_price,
            flash_desc=self.ticket_obj.desc,
            count=purchase_count,
            amount=purchase_amount,
            ticket=self.ticket_obj,
        )

        return order_obj



