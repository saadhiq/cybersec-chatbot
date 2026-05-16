from django.urls import path
from . import views

urlpatterns = [
    path('sessions/', views.list_sessions, name='list_sessions'),
    path('<int:session_id>/summarize/', views.summarize_session, name='summarize_session'),
]