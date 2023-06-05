from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, exceptions
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers

class InitiateComplianceViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = models.InitiateComplianceRequest.objects.all()
    serializer_class = serializers.InitiateComplianceRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        compliance_request = self.perform_create(serializer)
        response = models.InitiateComplianceResponse.objects.get_or_create(
            compliance_request_id = compliance_request.id
        )
        response.compliance_types = {
            compliance_request.compliance_types: compliance_request.compliance_types
        }
        response.next_step_api_endpoint = "compliance/submit/"
        response.next_step_http_method = "POST"
        submit_requ_body = models.SubmitComplianceRequest.objects.get_or_create(
            compliance_request_id = compliance_request.id
        )
        submit_requ_body.country = compliance_request.host_location.country
        response.next_step_request_body = {
            "compliance_request_id": compliance_request.id
        }
        response.save()
        print(response.compliance_request_id)

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
        print(exc)
        if isinstance(exc, exceptions.APIException) and hasattr(exc, 'status_code'):
            if exc.status_code == status.HTTP_400_BAD_REQUEST:
                return self.handle_error(status.HTTP_400_BAD_REQUEST, 'Invalid request')
            elif exc.status_code == status.HTTP_401_UNAUTHORIZED:
                return self.handle_error(status.HTTP_401_UNAUTHORIZED, 'Invalid authentication credentials')
            elif exc.status_code == status.HTTP_403_FORBIDDEN:
                return self.handle_error(status.HTTP_403_FORBIDDEN, 'Not authorized to perform the requested operation')
            elif exc.status_code == status.HTTP_404_NOT_FOUND:
                return self.handle_error(status.HTTP_404_NOT_FOUND, 'Requested resource could not be found')
            elif exc.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                return self.handle_error(status.HTTP_429_TOO_MANY_REQUESTS, 'Too many requests made quickly, rate limit exceeded')
            elif exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
                return self.handle_error(status.HTTP_500_INTERNAL_SERVER_ERROR, "Something is wrong on Cozm Travel's end")
            elif exc.status_code == status.HTTP_502_BAD_GATEWAY:
                return self.handle_error(status.HTTP_502_BAD_GATEWAY, 'Received an invalid response from the upstream server. Please try again later.')
        
        return self.handle_error(status.HTTP_500_INTERNAL_SERVER_ERROR, 'An unexpected error occurred')

    def handle_error(self, status_code, message):
        error_data = {
            'status': 'error',
            'message': message
        }

        return Response(error_data, status=status_code)