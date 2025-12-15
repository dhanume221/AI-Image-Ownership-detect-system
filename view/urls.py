from django.urls import path
from .views import RegisterContentView, VerifyOwnershipView

urlpatterns = [
    path('api/register/', RegisterContentView.as_view(), name='register_content'),
    path('api/verify/', VerifyOwnershipView.as_view(), name='verify_ownership'),
]
