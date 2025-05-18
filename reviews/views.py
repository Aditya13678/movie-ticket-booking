from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Review_table
from movies.models import Movie
from django.contrib.auth.decorators import login_required

@login_required
def submit_review(request, slug):
    movie = Movie.objects.filter(slug=slug).first()

    if not movie:
        return HttpResponse("Movie not found.", status=400)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')

        Review_table.objects.create(
            user_id=request.user,
            movie=movie,
            rating=rating,
            review_text=review_text
        )

        return redirect('search', slug=slug)

    return render(request, 'reviews/add_review.html', {'movie': movie})
        



