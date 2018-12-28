from django.shortcuts import render
from catalog.models import Video, Course
from django.views import generic

def index(request):
    """View function for home page"""
    num_videos = Video.objects.all().count()
    num_courses = Course.objects.all().count()

    context = {
        'num_videos': num_videos,
        'num_courses': num_courses,
    }

    return render(request, 'index.html', context=context)

