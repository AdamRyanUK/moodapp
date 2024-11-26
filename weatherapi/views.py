from django.shortcuts import render
import requests
from .models import DailyForecast, WeatherFeedback
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from datetime import date

@method_decorator(csrf_exempt, name='dispatch')
class SubmitFeedbackView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        try:
            rating = int(request.POST.get('rating'))
            if rating not in range(1, 6):
                return JsonResponse({'error': 'Invalid rating'}, status=400)

            today = date.today()

            feedback, created = WeatherFeedback.objects.update_or_create(
                user=request.user,
                date=today,
                defaults={'rating': rating}
            )
            return JsonResponse({'success': True, 'created': created})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)