import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from django.conf import settings

def get_mailchimp_client():
    client = MailchimpMarketing.Client()
    client.set_config({"api_key": settings.MAILCHIMP_API_KEY, "server": "usX"})  # Replace "usX" with your Mailchimp server prefix (e.g., "us21")
    return client

def add_subscriber(email):
    client = get_mailchimp_client()
    try:
        response = client.lists.add_list_member(
            settings.MAILCHIMP_AUDIENCE_ID,
            {
                "email_address": email,
                "status": "subscribed",  # "subscribed", "pending", or "unsubscribed"
            },
        )
        return response
    except ApiClientError as error:
        print("Error adding subscriber:", error.text)
        return None
