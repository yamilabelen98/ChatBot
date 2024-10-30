from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_view, name='chat'),
    path('process/', views.process_message, name='process_message'),
    path('history/', views.get_conversation_history, name='conversation_history'),
]