from rest_framework import serializers
from . import models

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ['id', 'country', 'city', 'zip_code', 'street']


class TravelDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TravelDate
        fields = ['id', 'departure_date', 'return_date']


class TripDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TripDetail
        fields = ['id', 'purpose', 'duration']


class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Passport
        fields = ['id', 'number', 'expiry_date']


class InitiateComplianceRequestSerializer(serializers.ModelSerializer):
    home_location = LocationSerializer()
    host_location = LocationSerializer()
    travel_dates = TravelDateSerializer()
    passport = PassportSerializer()
    trip_details = TripDetailSerializer()

    class Meta:
        model = models.InitiateComplianceRequest
        fields = ['id', 'home_location', 'host_location', 'travel_dates', 'nationality', 'passport', 'trip_details', 'compliance_types']

    def create(self, validated_data):
        home_location_data = validated_data.pop('home_location')
        host_location_data = validated_data.pop('host_location')
        travel_dates_data = validated_data.pop('travel_dates')
        passport_data = validated_data.pop('passport')
        trip_details_data = validated_data.pop('trip_details')

        home_location = models.Location.objects.create(**home_location_data)
        host_location = models.Location.objects.create(**host_location_data)
        travel_dates = models.TravelDate.objects.create(**travel_dates_data)
        passport = models.Passport.objects.create(**passport_data)
        trip_details = models.TripDetail.objects.create(**trip_details_data)

        compliance_request = models.InitiateComplianceRequest.objects.create(
            home_location=home_location,
            host_location=host_location,
            travel_dates=travel_dates,
            passport=passport,
            trip_details=trip_details,
            **validated_data
        )

        return compliance_request
    

class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employer
        fields = ['name', 'address', 'contact_number']


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmergencyContact
        fields = ['name', 'contact_number']


class PersonalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonalInformation
        fields = ['name', 'nationality', 'passport_number']


class SocialSecurityInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SocialSecurityInfo
        fields = ['coverage_start_date', 'coverage_end_date', 'certificate_number', 'issuing_authority']


class PWNDataSerializer(serializers.ModelSerializer):
    employer = EmployerSerializer()
    emergency_contact = EmergencyContactSerializer()
    personal_information = PersonalInformationSerializer()

    class Meta:
        model = models.PWNData
        fields = ['personal_information', 'home_location', 'host_location', 'employer', 'travel_dates',
                  'trip_purpose', 'duration', 'visa_type', 'previous_visits', 'emergency_contact']
        

class SSDataSerializer(serializers.ModelSerializer):
    employer = EmployerSerializer()
    personal_information = PersonalInformationSerializer()
    social_security_info = SocialSecurityInfoSerializer()

    class Meta:
        model = models.SSData
        fields = ['personal_information', 'employer', 'social_security_info']


class GovernmentPortalDataSerializer(serializers.ModelSerializer):
    pwn = PWNDataSerializer()
    ss = SSDataSerializer()

    class Meta:
        model = models.GovernmentPortalData
        fields = ['pwn', 'ss']


class InitiateComplianceResponseSerializer(serializers.ModelSerializer):
    government_portal_data = GovernmentPortalDataSerializer()

    class Meta:
        model = models.InitiateComplianceResponse
        fields = ['status', 'message', 'compliance_request_id', 'compliance_types',
                  'next_step_api_endpoint', 'next_step_http_method', 'next_step_request_body',
                  'government_portal_data']