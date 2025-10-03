from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import Movie, Review, Petition, PetitionVote

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment']!= '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term, amount_left__gt=0)
    else:
        movies = Movie.objects.filter(amount_left__gt=0)
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html',
                  {'template_data': template_data})

def petitions_index(request):
    petitions = Petition.objects.all()
    
    # Add voting status for each petition if user is authenticated
    if request.user.is_authenticated:
        for petition in petitions:
            petition.user_has_voted = petition.has_user_voted(request.user)
    else:
        for petition in petitions:
            petition.user_has_voted = False
    
    template_data = {
        'title': 'Movie Petitions',
        'petitions': petitions
    }
    return render(request, 'movies/petitions_index.html', {'template_data': template_data})

@login_required
def petition_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        
        if title and description:
            petition = Petition(
                title=title,
                description=description,
                image=image,
                created_by=request.user
            )
            petition.save()
            messages.success(request, 'Petition created successfully!')
            return redirect('movies.petitions_index')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    template_data = {
        'title': 'Create Movie Petition'
    }
    return render(request, 'movies/petition_create.html', {'template_data': template_data})

@login_required
def petition_vote(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    
    try:
        # Check if user has already voted
        existing_vote = PetitionVote.objects.filter(
            user=request.user,
            petition=petition
        ).first()
        
        if existing_vote:
            # User has voted, so remove the vote (unvote)
            existing_vote.delete()
            messages.success(request, 'Your vote has been removed!')
        else:
            # User hasn't voted, so add the vote
            PetitionVote.objects.create(
                user=request.user,
                petition=petition
            )
            messages.success(request, 'Your vote has been recorded!')
            
    except IntegrityError:
        messages.error(request, 'An error occurred while processing your vote.')
    
    return redirect('movies.petitions_index')