# In yourapp/urls.py
from django.urls import path
from .views import SubmitFeedbackView

urlpatterns = [
    path('submit-feedback/', SubmitFeedbackView.as_view(), name='submit-feedback'),
]
