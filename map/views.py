from django.shortcuts import render
from cart.models import Item
from movies.models import Movie
from django.views.decorators.http import require_GET
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'map/index.html')

@require_GET
def top_movies_by_state(request):
    click_state = (request.GET.get("state") or  "").upper().strip()
    
    purchases = Item.objects.filter(state=click_state)
    totals = {}
    for item in purchases:
        if item.movie not in totals:
            totals[item.movie] = 0
        totals[item.movie] += item.quantity
    maxkey = ("N/A",0)
    for movie, count in totals.items():
        if count > maxkey[1]:
            maxkey = (movie, count)
    return JsonResponse({'state': click_state, "top": maxkey[0], 'fallback':False})