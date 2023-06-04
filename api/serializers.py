from rest_framework import serializers
from . import models

class InitiateComplianceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InitiateComplianceRequest
        fields = '__all__'