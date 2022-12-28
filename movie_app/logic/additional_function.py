from django.contrib.auth.decorators import user_passes_test
from django.conf import settings

from ..models import Movie, Genre


def get_years():
    return Movie.objects.filter(draft=False).values("year").distinct().order_by('year')


def get_genres():
    return Genre.objects.all()


def login_forbidden(function=None, redirect_field_name=None, redirect_to=settings.LOGIN_REDIRECT_URL):
    """
    Decorator for views that checks that the user is NOT logged in, redirecting
    to the homepage if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=redirect_to,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
