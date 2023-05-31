from django.http import JsonResponse


class NotFoundJsonResponse(JsonResponse):
    def __init__(self, *args, **kwargs):
        self.status_code = 404
        data = {
            "error_code": "404000",
            "error_message": "content not found",
        }
        super().__init__(data, *args, **kwargs)


class FormValidationFailJsonResponse(JsonResponse):
    def __init__(self, error_list=None, *args, **kwargs):
        if error_list is None:
            error_list = []
        self.status_code = 400
        data = {
            "error_code": "400000",
            "error_message": "form validation failed",
            "error_list": error_list,
        }
        super().__init__(data, *args, **kwargs)


class MethodNotAllowedJsonResponse(JsonResponse):
    def __init__(self, *args, **kwargs):
        self.status_code = 405
        data = {
            "error_code": "405000",
            "error_message": "request method is not allowed",
        }
        super().__init__(data, *args, **kwargs)


class UnauthorizedJsonResponse(JsonResponse):
    def __init__(self, *args, **kwargs):
        self.status_code = 401
        data = {
            "error_code": "401000",
            "error_message": "User unauthorized",
        }
        super().__init__(data, *args, **kwargs)


class ServerErrorJsonResponse(JsonResponse):
    def __init__(self, *args, **kwargs):
        self.status_code = 500
        data = {
            "error_code": "500000",
            "error_message": "Sorry, the server is busy. Please try again later",
        }
        super().__init__(data, *args, **kwargs)
