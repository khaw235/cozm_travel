from django.urls import path
from . import views

urlpatterns = [
    path('compliance/initiate/', views.InitiateComplianceViewSet.as_view({"post": "create"}), name="initiate--compliance"),
]
