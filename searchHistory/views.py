from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SearchHistory
import json
from django.db import IntegrityError


@csrf_exempt
def store_search_query(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query')
            if request.user.is_authenticated:
                SearchHistory.objects.create(user=request.user, query=query)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid request'})
            return JsonResponse({'status': 'success', 'message': 'Query saved'})
        except IntegrityError as e:
            if 'unique constraint' in str(e):
                return JsonResponse({'status': 'error', 'message': 'Duplicate entry: This search query has already been recorded for this user.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'An INTEGRITY ERROR occurred while saving the search query.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@csrf_exempt
def get_search_history(request):
    if request.user.is_authenticated:
        # Retrieve the last 10 search queries made by the user
        history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')[:10]
        history_data = [{'query': h.query, 'timestamp': h.timestamp} for h in history]
        return JsonResponse({'history': history_data})
    else:
        return JsonResponse({'history': []})  # Empty list if the user is not authenticated
