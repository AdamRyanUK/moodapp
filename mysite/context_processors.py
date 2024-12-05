from django.conf import settings
from authenticate.models import UserProfile

def add_user_status(request):
    return {
        'is_authenticated': request.user.is_authenticated,
    }


