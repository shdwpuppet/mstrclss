from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def staff_member_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    '''
    include this before view definitions or when .as_view is used in url files to require that users have is_staff be True
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url='/login/steam',
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator
