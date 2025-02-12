from django.http import JsonResponse
from django.conf import settings  # Import settings to access the API key
from mailchimp_transactional.api_client import ApiClientError
import mailchimp_transactional

mailchimp = mailchimp_transactional.Client(
    api_key=settings.MAILCHIMP_TRANSACTIONAL_API_KEY,
)

def send_view(request):
    message = {
        'from_email': 'admin@clearskyapp.io',
        'subject': 'My First Email',
        'text': 'Hey there, this email has been sent via Mailchimp Transactional API.',
        'to': [
            {
                'email': 'adam@clearskyapp.io',
                'type': 'to'
            },
        ]
    }
    try:
        response = mailchimp.messages.send({'message': message})
        return JsonResponse({
            'detail': 'Email has been sent',
            'response': response,
        })
    except ApiClientError as error:
        return JsonResponse({
            'detail': 'Something went wrong',
            'error': error.text,
        })


def mailchimp_transactional_ping_view(request):
    mailchimp = MailchimpTransactional.Client(settings.MAILCHIMP_TRANSACTIONAL_API_KEY)
    try:
        response = mailchimp.users.ping()
        return JsonResponse({
            'detail': 'Everything is working fine',
            'response': response,
        })
    except ApiClientError as error:
        return JsonResponse({
            'detail': 'Something went wrong',
            'error': error.text,
        })
