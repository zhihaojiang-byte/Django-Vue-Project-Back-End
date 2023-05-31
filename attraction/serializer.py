from system.serializer import ImageSerializer
from utils.serializer import BaseListPageSerializer, BaseSerializer


class AttractionListPageSerializer(BaseListPageSerializer):
    def item_to_dict(self, item) -> dict:
        return {
            'id': item.id,
            'name': item.name,
            'cover_img_url': item.cover_img.url,
            'rating': item.rating,
            'province': item.province,
            'city': item.city,
            'comment_count': item.comments_count,
        }


class AttractionDetailSerializer(BaseSerializer):
    def to_dict(self) -> dict:
        return {
            'id': self.obj.id,
            'name': self.obj.name,
            'address': self.obj.address,
            'banner_img_url': self.obj.banner_img.url,
            'rating': self.obj.rating,
            'province': self.obj.province,
            'city': self.obj.city,
            'comment_count': self.obj.comments_count,
            'images_count': self.obj.images_count,
        }


class CommentListPageSerializer(BaseListPageSerializer):
    def item_to_dict(self, item) -> dict:
        images = []
        for image in item.images.filter(is_valid=True):
            images.append(ImageSerializer(image).to_dict())

        return {
            'id': item.id,
            'user': {
                'user_id': item.user.id,
                'username': item.user.username,
            },
            'content': item.content,
            'rating': item.rating,
            'images': images,
            'create_at': item.create_at.strftime('%Y-%m-%d')
        }


class AttractionImagesPageSerializer(BaseListPageSerializer):
    def item_to_dict(self, item) -> dict:
        return {
            'id': item.id,
            'img_url': item.img.url,
            'name': item.name,
        }


class TicketListPageSerializer(BaseListPageSerializer):
    def item_to_dict(self, item) -> dict:
        return {
            'id': item.id,
            'name': item.name,
            'desc': item.desc,
            'price': item.price,
            'discount': item.discount,
            'stock': item.stock,
            'sell_price': item.sell_price,
            'on_sale': item.on_sale,
        }


class AttractionInfoSerializer(BaseSerializer):
    def to_dict(self) -> dict:
        return {
            'info': self.obj.info,
        }


class TicketSerializer(BaseSerializer):
    def to_dict(self) -> dict:
        return {
            'id': self.obj.id,
            'name': self.obj.name,
            'desc': self.obj.desc,
            'price': self.obj.price,
            'discount': self.obj.discount,
            'stock': self.obj.stock,
            'sell_price': self.obj.sell_price,
            'on_sale': self.obj.on_sale,
        }


class TicketInfoSerializer(BaseSerializer):
    def to_dict(self) -> dict:
        return {
            'info': self.obj.info,
        }
