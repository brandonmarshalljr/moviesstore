from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    amount_left = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Number of copies available (optional)",
        default=None
    )
    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
        
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
    
class Petition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='petitions/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_petitions')
    created_at = models.DateTimeField(auto_now_add=True)
    voters = models.ManyToManyField(User, through='PetitionVote', related_name='voted_petitions')
    
    def vote_count(self):
        return self.petitionvote_set.count()
    
    def has_user_voted(self, user):
        if not user.is_authenticated:
            return False
        return self.petitionvote_set.filter(user=user).exists()
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class PetitionVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'petition')