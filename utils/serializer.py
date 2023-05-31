from abc import ABCMeta, abstractmethod


# an abstract class , take an object and return a dictionary
class BaseSerializer(object, metaclass=ABCMeta):

    def __init__(self, obj):
        self.obj = obj

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class MetaSerializer(object):
    def __init__(self, current_page, page_count, total_count, **kwargs):
        self.current_page = current_page
        self.page_count = page_count
        self.total_count = total_count

    def to_dict(self) -> dict:
        return {
            "current_page": self.current_page,
            "page_count": self.page_count,
            "total_count": self.total_count,
        }


class BaseListPageSerializer(object, metaclass=ABCMeta):

    def __init__(self, page_obj):
        self.page_obj = page_obj
        self.paginator = self.page_obj.paginator
        self.object_list = self.page_obj.object_list

    @abstractmethod
    def item_to_dict(self, item) -> dict:
        pass

    def to_dict(self) -> dict:
        data = {
            'meta': MetaSerializer(current_page=self.page_obj.number, page_count=self.paginator.num_pages,
                                   total_count=self.paginator.count).to_dict(),
            'object': []
        }

        for item in self.object_list:
            data['object'].append(self.item_to_dict(item))

        return data
