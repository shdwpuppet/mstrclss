from .models import Attendee


def attendee_create(strategy, details, user=None, *args, **kwargs):
    Attendee.objects.get_or_create(user=user)