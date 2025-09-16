from django.contrib import admin
from .models import Movie, Review

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
    list_display = ['name', 'amount_left']
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.amount_left == 0:
            return ['amount_left']
        return []

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)