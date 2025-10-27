"""
API Views for job fraud detection
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import JobPostingSerializer, PredictionResponseSerializer
from .utils import predictor


class PredictJobFraudView(APIView):
    """
    API endpoint for predicting job fraud
    
    POST /api/predict/
    """
    
    def post(self, request):
        """
        Handle POST request for job fraud prediction
        
        Request body should contain job posting details
        Returns prediction result with fraud probability
        """
        try:
            # Validate input data
            serializer = JobPostingSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response(
                    {'error': 'Invalid input data', 'details': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Make prediction
            input_data = serializer.validated_data
            prediction_result = predictor.predict(input_data)
            
            # Validate output
            response_serializer = PredictionResponseSerializer(data=prediction_result)
            if response_serializer.is_valid():
                return Response(
                    {
                        'success': True,
                        'data': response_serializer.validated_data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Invalid prediction result'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        except Exception as e:
            return Response(
                {'error': 'Prediction failed', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HealthCheckView(APIView):
    """
    API endpoint for health check
    
    GET /api/health/
    """
    
    def get(self, request):
        """
        Simple health check endpoint
        """
        return Response(
            {
                'status': 'healthy',
                'message': 'Job Fraud Detection API is running',
                'model_loaded': predictor.model is not None
            },
            status=status.HTTP_200_OK
        )


class ModelInfoView(APIView):
    """
    API endpoint for model information
    
    GET /api/model-info/
    """
    
    def get(self, request):
        """
        Return information about the loaded model
        """
        try:
            info = {
                'model_type': type(predictor.model).__name__,
                'features_count': predictor.model.n_features_in_ if hasattr(predictor.model, 'n_features_in_') else 'N/A',
                'tfidf_features': predictor.tfidf.max_features if hasattr(predictor.tfidf, 'max_features') else 'N/A',
            }
            return Response(info, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )