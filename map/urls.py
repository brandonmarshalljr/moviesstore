from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='map.index'),
    #path('region/', views.region, name='map.region')
]