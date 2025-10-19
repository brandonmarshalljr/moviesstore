from django.db import models
from movies.models import Movie

# Create your models here.
from django.contrib.auth.models import User

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.user.username
    #movie_data = models.ManyToManyField(Movie)
    #state = models.CharField(max_length=16, default="Georgia")
    

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
    STATES = [
        ('Alabama','Alabama'),
        ('Alaska','Alaska'),
        ('Arizona','Arizona'),
        ('Arkansas','Arkansas'),
        ('California','California'),
        ('Colorado','Colorado'),
        ('Connecticut','Connecticut'),
        ('Delaware','Delaware'),
        ('District of Columbia','District of Columbia'),
        ('Florida','Florida'),
        ('Georgia','Georgia'),
        ('Hawaii','Hawaii'),
        ('Idaho','Idaho'),
        ('Illinois','Illinois'),
        ('Indiana','Indiana'),
        ('Iowa','Iowa'),
        ('Kansas','Kansas'),
        ('Kentucky','Kentucky'),
        ('Louisiana','Louisiana'),
        ('Maine','Maine'),
        ('Maryland','Maryland'),
        ('Massachussetts','Massachussetts'),
        ('Michigan','Michigan'),
        ('Minnesota','Minnesota'),
        ('Mississippi','Mississippi'),
        ('Missouri','Missouri'),
        ('Montana','Montana'),
        ('Nebraska','Nebraska'),
        ('Nevada','Nevada'),
        ('New Hampshire','New Hampshire'),
        ('New Jersey','New Jersey'),
        ('New Mexico','New Mexico'),
        ('New York','New York'),
        ('North Carolina','North Carolina'),
        ('North Dakota','North Dakota'),
        ('Ohio','Ohio'),
        ('Oklahoma','Oklahoma'),
        ('Oregon','Oregon'),
        ('Pennsylvania','Pennsylvania'),
        ('Rhode Island','Rhode Island'),
        ('South Carolina','South Carolina'),
        ('South Dakota','South Dakota'),
        ('Tennessee','Tennessee'),
        ('Texas','Texas'),
        ('Utah','Utah'),
        ('Vermont','Vermont'),
        ('Virginia','Virginia'),
        ('Washington','Washington'),
        ('West Virginia','West Virginia'),
        ('Wisconsin','Wisconsin'),
        ('Wyoming','Wyoming'),
    ]
    state = models.CharField(max_length=20, default="Georgia", choices=STATES)
    