from system.serializer import ImageSerializer
from utils.serializer import BaseListPageSerializer, BaseSerializer


class UserSerializer(BaseSerializer):
    def to_dict(self) -> dict:
        return {
            'username': self.obj.username,
            'email': self.obj.email,
            'avatar': self.obj.avatar.url,
        }

