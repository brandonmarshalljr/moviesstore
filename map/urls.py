from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='map.index'),
    #path('region/', views.region, name='map.region')
    path('api/top-by-state', views.top_movies_by_state, name='map.top_by_state')
]