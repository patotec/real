from django.urls import path
from . import views

app_name = 'indexurl'
urlpatterns = [
	path('', views.myindex, name='index'),
	path('contact/',  views.mycontact ,name='contact'),
	path('about/',  views.myabout ,name='about'),
	path('listing/<slug>',  views.myprop ,name='list'),


    ]

