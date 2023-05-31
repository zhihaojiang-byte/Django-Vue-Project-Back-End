from utils.serializer import BaseSerializer


class ImageSerializer(BaseSerializer):
    def to_dict(self) -> dict:
        return {
            'img_url': self.obj.img.url,
            'name': self.obj.name,
        }
