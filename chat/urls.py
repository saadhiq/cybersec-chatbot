from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_session, name='start_session'),
    path('<int:session_id>/message/', views.send_message, name='send_message'),
    path('<int:session_id>/history/', views.get_history, name='get_history'),
]