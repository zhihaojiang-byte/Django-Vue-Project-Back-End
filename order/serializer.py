from utils.serializer import BaseSerializer, BaseListPageSerializer


class OrderItemSerializer(BaseSerializer):
    def to_dict(self) -> dict:
        obj = self.obj
        return {
            'pk': obj.pk,
            'user': obj.user.pk,
            'flash_name': obj.flash_name,
            'flash_image': obj.flash_image.url,
            'flash_price': obj.flash_price,
            'flash_discount': obj.flash_discount,
            'flash_sell_price': obj.flash_sell_price,
            'flash_desc': obj.flash_desc,
            'count': obj.count,
            'amount': obj.amount,
            'status': obj.status,
            'ticket': obj.ticket.pk,
        }


class OrderDetailSerializer(BaseSerializer):
    def to_dict(self) -> dict:
        obj = self.obj
        order_items = []
        for item in obj.order_items.all():
            order_items.append(OrderItemSerializer(item).to_dict())
        return {
            'sn': obj.sn,
            'user': obj.user.pk,
            'purchase_count': obj.purchase_count,
            'purchase_amount': obj.purchase_amount,
            'full_name': obj.full_name,
            'status': obj.status,
            'create_at': obj.create_at,
            'order_items': order_items,
        }


class OrderListSerializer(BaseListPageSerializer):
    def item_to_dict(self, item) -> dict:
        first_order_item = item.order_items.first()
        return {
            'sn': item.sn,
            'user': item.user.pk,
            'purchase_count': item.purchase_count,
            'purchase_amount': item.purchase_amount,
            'full_name': item.full_name,
            'status': item.status,
            'create_at': item.create_at,
            'first_order_item': OrderItemSerializer(first_order_item).to_dict(),
        }
