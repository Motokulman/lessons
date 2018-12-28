from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    # path('', RedirectView.as_view(url='/catalog/', permanent=True)),
   
]

#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)