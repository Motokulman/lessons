from django.shortcuts import render
from catalog.models import Video, Course, Pupil, Lesson
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required

#new user creation
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
#and this too
from catalog.forms import CustomSignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.contrib import auth

def index(request):
    """View function for home page"""
    num_videos = Video.objects.all().count()
    num_courses = Course.objects.all().count()

    context = {
        'num_videos': num_videos,
        'num_courses': num_courses,
    }

    return render(request, 'index.html', context=context)

def about(request):
    """View function for about page"""

    context = {

    }

    return render(request, 'about.html', context=context)

def user(request):
    """View function for user page"""

    context = {

    }

    return render(request, 'user.html', context=context)


class VideoListView(generic.ListView):
    model = Video

class CourseListView(generic.ListView):
    model = Course

class PupilsCustomerListView(generic.ListView):
    model = Pupil

    def get_queryset(self):
        return Pupil.objects.filter(customer=self.request.user)

#new user form
class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)

#new user form2
def signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            #form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            # Create user and save to the database
            user = User.objects.create_user(username, email, password)
            user.save()
            user = authenticate(username=username, password=password)
            auth.login(request, user)
            #return redirect('index')
            if user is not None:
                return render(request, 'index.html') 
            else:
                return HttpResponse("fail")
            #return render(request, 'index.html')           
    else:
        form = CustomSignUpForm()
    return render(request, 'signup.html', {'form': form})








# class SubmittedCoursesByPeopleListView(LoginRequiredMixin,generic.ListView):
#     """Generic class-based view listing courses on submit to current user's pupil."""
#     model = Course
#     template_name ='catalog/course_list_submit_pupil.html'
#     paginate_by = 10
    
#    def get_queryset(self):
#        return Course.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')



