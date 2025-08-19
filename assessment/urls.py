from django.urls import path
from . import views

urlpatterns = [
    path('', views.session1, name='session_form'),  # root redirects to session1
    path('session1/', views.session1, name='session1'),
    path('session2/', views.session2, name='session2'),
    path('session3/', views.session3, name='session3'),\
    path('session4/', views.session4, name='session4'),
    path('summary/', views.summary, name='summary'),
]
