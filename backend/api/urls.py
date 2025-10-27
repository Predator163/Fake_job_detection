"""
URL configuration for API endpoints
"""
from django.urls import path
from .views import PredictJobFraudView, HealthCheckView, ModelInfoView

urlpatterns = [
    path('predict/', PredictJobFraudView.as_view(), name='predict-fraud'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('model-info/', ModelInfoView.as_view(), name='model-info'),
]