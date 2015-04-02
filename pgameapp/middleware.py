__author__ = 'Jailbreaker'

# http://stackoverflow.com/questions/3006753/how-to-convert-request-user-into-a-proxy-auth-user-class

from pgameapp.models import User


class CastToCustomUserMiddleware(object):
    """
    Middleware that casts user in request to a proxy model
    """
    # noinspection PyMethodMayBeStatic
    def process_request(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated():
            request.user.__class__ = User