from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import Movie, Review, Petition, PetitionVote, Rating

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
    
    # Get user's rating if authenticated
    user_rating = None
    if request.user.is_authenticated:
        user_rating = movie.get_user_rating(request.user)
    
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['user_rating'] = user_rating
    return render(request, 'movies/show.html',
                  {'template_data': template_data})

@login_required
def rate_movie(request, id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=id)
        rating_value = request.POST.get('rating')
        
        if rating_value in ['up', 'down']:
            # Check if user has already rated this movie
            existing_rating = Rating.objects.filter(user=request.user, movie=movie).first()
            
            if existing_rating:
                if existing_rating.rating == rating_value:
                    # Same rating clicked, remove it
                    existing_rating.delete()
                    messages.success(request, 'Your rating has been removed!')
                else:
                    # Different rating clicked, update it
                    existing_rating.rating = rating_value
                    existing_rating.save()
                    rating_text = 'thumbs up' if rating_value == 'up' else 'thumbs down'
                    messages.success(request, f'Your rating has been updated to {rating_text}!')
            else:
                # New rating
                Rating.objects.create(user=request.user, movie=movie, rating=rating_value)
                rating_text = 'thumbs up' if rating_value == 'up' else 'thumbs down'
                messages.success(request, f'You gave this movie a {rating_text}!')
        else:
            messages.error(request, 'Invalid rating value.')
    
    return redirect('movies.show', id=id)

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