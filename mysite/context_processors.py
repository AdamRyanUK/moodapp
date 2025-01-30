from django.conf import settings


def add_user_status(request):
    return {
        'is_authenticated': request.user.is_authenticated,
    }


