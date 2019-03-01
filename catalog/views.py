from django.shortcuts import render
from catalog.models import Video, Course, Pupil, Lesson
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required

def index(request):
    """View function for home page"""
    num_videos = Video.objects.all().count()
    num_courses = Course.objects.all().count()

    context = {
        'num_videos': num_videos,
        'num_courses': num_courses,
    }

    return render(request, 'index.html', context=context)


class VideoListView(generic.ListView):
    model = Video

class CourseListView(generic.ListView):
    model = Course

class PupilsCustomerListView(generic.ListView):
    model = Pupil

    def get_queryset(self):
        return Pupil.objects.filter(customer=self.request.user)

# class SubmittedCoursesByPeopleListView(LoginRequiredMixin,generic.ListView):
#     """Generic class-based view listing courses on submit to current user's pupil."""
#     model = Course
#     template_name ='catalog/course_list_submit_pupil.html'
#     paginate_by = 10
    
#    def get_queryset(self):
#        return Course.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')



