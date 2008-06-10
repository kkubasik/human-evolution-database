"""Custom middleware.  Some of this may be generally useful."""

from google.appengine.api import users


class AddUserToRequestMiddleware(object):
    def process_request(self, request):
        request.user = users.get_current_user()
        request.user_is_admin = users.is_current_user_admin()
