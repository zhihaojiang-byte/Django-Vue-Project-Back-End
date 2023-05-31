from functools import wraps

from utils.response import UnauthorizedJsonResponse


# a decorator for the view that need user login
def login_require(func):

    @wraps(func)
    def _wrapper(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return UnauthorizedJsonResponse()
        return func(request, *args, **kwargs)

    return _wrapper

