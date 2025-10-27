"""
Serializers for API request/response validation
"""
from rest_framework import serializers


class JobPostingSerializer(serializers.Serializer):
    """
    Serializer for job posting input data
    """
    title = serializers.CharField(max_length=500, required=False, allow_blank=True)
    location = serializers.CharField(max_length=200, required=False, allow_blank=True)
    department = serializers.CharField(max_length=200, required=False, allow_blank=True)
    salary_range = serializers.CharField(max_length=100, required=False, allow_blank=True)
    company_profile = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    requirements = serializers.CharField(required=False, allow_blank=True)
    benefits = serializers.CharField(required=False, allow_blank=True)
    telecommuting = serializers.IntegerField(min_value=0, max_value=1, required=False, default=0)
    has_company_logo = serializers.IntegerField(min_value=0, max_value=1, required=False, default=0)
    has_questions = serializers.IntegerField(min_value=0, max_value=1, required=False, default=0)
    employment_type = serializers.CharField(max_length=100, required=False, allow_blank=True)
    required_experience = serializers.CharField(max_length=100, required=False, allow_blank=True)
    required_education = serializers.CharField(max_length=100, required=False, allow_blank=True)
    industry = serializers.CharField(max_length=200, required=False, allow_blank=True)
    function = serializers.CharField(max_length=200, required=False, allow_blank=True)


class PredictionResponseSerializer(serializers.Serializer):
    """
    Serializer for prediction response
    """
    prediction = serializers.CharField()
    fraud_probability = serializers.FloatField()
    legitimate_probability = serializers.FloatField()
    risk_level = serializers.CharField()
    is_fraudulent = serializers.BooleanField()