from django.shortcuts import render,redirect
from .models import Movie,search_movies_by_name
from .forms import Search_movie
from django.http import HttpResponse
from reviews.models import Review_table
from django.db.models import Avg

# Create your views here.


def search_movie(request,slug):
    if Movie.objects.filter(slug=slug).exists():

        movie=Movie.objects.get(slug=slug)
        if Review_table.objects.filter(movie=movie).exists():
            review=Review_table.objects.filter(movie=movie)
            no_user=review.count()
            rating=review.aggregate(avg_rating=Avg('rating'))

            context={
                'name':movie,
                'ratings':rating['avg_rating'],
                'no_users':no_user,
                'reviews':review
            }
            return render(request,'movies/movie_name2.html',context)
    return render(request,'movies/404.html',status=404)




# def search_moviebyname(request):
#     s=Search_movie()
#     context={
#         'moviename':s
#     }

#     if request.method=='POST':
#         sa=Search_movie(request.POST)
#         return redirect(f'/movies/search/{sa}')
#     return render(request,'movies/sample.html',context)
