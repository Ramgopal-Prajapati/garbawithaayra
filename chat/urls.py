from django.urls import path
from . import views

urlpatterns = [
    path('<int:match_id>/', views.chat_view, name='chat_view'),
    path('<int:match_id>/send/', views.send_message, name='send_message'),
    path('react/<int:message_id>/', views.react_message, name='react_message'),
]
