from django.urls import path
from . import views

urlpatterns = [
    path("readings/", views.risk_readings, name="risk_readings"),
    path("latest/", views.latest_risk, name="latest_risk"),
]