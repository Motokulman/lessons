from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('videos/', views.VideoListView.as_view(), name='videos'),
    path('courses/', views.CourseListView.as_view(), name='courses'),
  
]

#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)