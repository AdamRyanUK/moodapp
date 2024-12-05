from django.http import JsonResponse
from .services import get_city_suggestions

def city_autocomplete(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'error': 'Missing query parameter'}, status=400)
    suggestions = get_city_suggestions(query)
    return JsonResponse({'suggestions': suggestions})

