from django.contrib.contenttypes.models import ContentType
from django.db import models

from attraction.models import Ticket
from utils.models import BaseModel
from account.models import User


class OrderStatus(models.IntegerChoices):
    SUBMIT = 1
    PAID = 2
    CANCELED = 3


# 订单, 记录用户, 商品个数, 总金额, 购买者真实姓名, 订单状态;
class Order (BaseModel):
    sn = models.CharField('order number', max_length=32)
    user = models.ForeignKey(User, related_name="orders", on_delete=models.PROTECT)
    purchase_count = models.IntegerField('purchase count', default=1)
    purchase_amount = models.FloatField('purchase amount')
    full_name = models.CharField(max_length=32)
    status = models.SmallIntegerField(choices=OrderStatus.choices, default=OrderStatus.SUBMIT)


class OrderItem(BaseModel):
    user = models.ForeignKey(User, related_name="order_items", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    flash_name = models.CharField('item name', max_length=120)
    flash_image = models.ImageField('item image')
    flash_price = models.FloatField(default=0)
    flash_discount = models.FloatField(default=0)
    flash_sell_price = models.FloatField(default=0)
    flash_desc = models.CharField(max_length=120, null=True, blank=True)
    count = models.PositiveIntegerField(default=0)
    amount = models.FloatField(default=0)
    status = models.SmallIntegerField(choices=OrderStatus.choices, default=OrderStatus.SUBMIT)
    ticket = models.ForeignKey(Ticket, related_name="order_items", on_delete=models.SET_NULL, blank=True, null=True)

