from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers

class InitiateComplianceViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = models.InitiateComplianceRequest.objects.all()
    serializer_class = serializers.InitiateComplianceRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Perform any necessary data processing or validation based on the compliance request

        compliance_request = self.perform_create(serializer)
        response_serializer = serializers.InitiateComplianceResponseSerializer(compliance_request)

        response_data = {
            'status': 'success',
            'message': 'Compliance request initiated successfully',
            'data': response_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        return serializer.save()

    def handle_exception(self, exc):
        if isinstance(exc, status.HTTP_400_BAD_REQUEST):
            return self.handle_error(status.HTTP_400_BAD_REQUEST, 'Invalid request')
        elif isinstance(exc, status.HTTP_401_UNAUTHORIZED):
            return self.handle_error(status.HTTP_401_UNAUTHORIZED, 'Invalid authentication credentials')
        elif isinstance(exc, status.HTTP_403_FORBIDDEN):
            return self.handle_error(status.HTTP_403_FORBIDDEN, 'Not authorized to perform the requested operation')
        elif isinstance(exc, status.HTTP_404_NOT_FOUND):
            return self.handle_error(status.HTTP_404_NOT_FOUND, 'Requested resource could not be found')
        elif isinstance(exc, status.HTTP_429_TOO_MANY_REQUESTS):
            return self.handle_error(status.HTTP_429_TOO_MANY_REQUESTS, 'Too many requests made quickly, rate limit exceeded')
        elif isinstance(exc, status.HTTP_500_INTERNAL_SERVER_ERROR):
            return self.handle_error(status.HTTP_500_INTERNAL_SERVER_ERROR, "Something is wrong on Cozm Travel's end")
        elif isinstance(exc, status.HTTP_502_BAD_GATEWAY):
            return self.handle_error(status.HTTP_502_BAD_GATEWAY, 'Received an invalid response from the upstream server. Please try again later.')
        else:
            return self.handle_error(status.HTTP_500_INTERNAL_SERVER_ERROR, 'An unexpected error occurred')

    def handle_error(self, status_code, message):
        error_data = {
            'status': 'error',
            'message': message
        }

        return Response(error_data, status=status_code)