from django.apps import AppConfig


class NewsletterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "newsletter"

class YourAppConfig(AppConfig):
    name = 'newsletter'

    def ready(self):
        import newsletter.signals
