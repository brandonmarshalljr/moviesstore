from django.contrib import admin
from .models import Movie, Review, Petition, PetitionVote

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
    list_display = ['name', 'amount_left']
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.amount_left == 0:
            return ['amount_left']
        return []

class PetitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'vote_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description', 'created_by__username']
    readonly_fields = ['created_at', 'vote_count']
    
    def vote_count(self, obj):
        return obj.vote_count()
    vote_count.short_description = 'Votes'

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(Petition, PetitionAdmin)
admin.site.register(PetitionVote)