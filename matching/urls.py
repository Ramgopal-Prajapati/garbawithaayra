from django.urls import path
from . import views

urlpatterns = [
    path('api/requests/send/<int:receiver_id>/', views.send_request, name='send_request'),
    path('api/requests/accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('api/requests/decline/<int:request_id>/', views.decline_request, name='decline_request'),
    path('api/requests/unmatch/<int:match_id>/', views.unmatch, name='unmatch'),
]
