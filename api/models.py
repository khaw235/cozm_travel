from django.db import models

# Create your models here.
class Location(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20, editable=False)
    street = models.CharField(max_length=255, editable=False)


class TravelDate(models.Model):
    departure_date = models.DateField()
    return_date = models.DateField()


class TripDetail(models.Model):
    purpose = models.CharField(max_length=255)
    duration = models.IntegerField()


class PersonalInformation(models.Model):
    name = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    passport_number = models.CharField(max_length=255)


class Passport(models.Model):
    number = models.CharField(max_length=255)
    expiry_date = models.DateField()


class Employer(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)


class EmergencyContact(models.Model):
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)


class SocialSecurityInfo(models.Model):
    coverage_start_date = models.DateField()
    coverage_end_date = models.DateField()
    certificate_number = models.CharField(max_length=255)
    issuing_authority = models.CharField(max_length=255)


class Employee(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    birthday = models.DateField()
    home_country = models.CharField(max_length=255)


class PWNField(models.Model):
    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)
    home_location = models.ForeignKey(Location, related_name='pwn_fields_home', on_delete=models.CASCADE)
    host_location = models.ForeignKey(Location, related_name='pwn_fields_host', on_delete=models.CASCADE)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    travel_dates = models.ForeignKey(TravelDate, on_delete=models.CASCADE)
    trip_purpose = models.CharField(max_length=255)
    duration = models.IntegerField()
    visa_type = models.CharField(max_length=255)
    previous_visits = models.BooleanField()
    emergency_contact = models.ForeignKey(EmergencyContact, on_delete=models.CASCADE)


class PWNData(models.Model):
    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)
    home_location = models.ForeignKey(Location, related_name='pwn_data_home', on_delete=models.CASCADE)
    host_location = models.ForeignKey(Location, related_name='pwn_data_host', on_delete=models.CASCADE)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    travel_dates = models.ForeignKey(TravelDate, on_delete=models.CASCADE)
    trip_purpose = models.CharField(max_length=255)
    duration = models.IntegerField()
    visa_type = models.CharField(max_length=255)
    previous_visits = models.BooleanField()
    emergency_contact = models.ForeignKey(EmergencyContact, on_delete=models.CASCADE)


class SSField(models.Model):
    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    social_security_info = models.ForeignKey(SocialSecurityInfo, on_delete=models.CASCADE)


class SSData(models.Model):
    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    social_security_info = models.ForeignKey(SocialSecurityInfo, on_delete=models.CASCADE)


class BVField(models.Model):
    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    social_security_info = models.ForeignKey(SocialSecurityInfo, on_delete=models.CASCADE)


class GovernmentPortalData(models.Model):
    pwn = models.ForeignKey(PWNData, on_delete=models.CASCADE)
    ss = models.ForeignKey(SSData, on_delete=models.CASCADE)


class Request(models.Model):
    compliance_request_id = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    host_country = models.CharField(max_length=255)
    issue = models.CharField(max_length=255)
    created_date = models.DateField()
    last_updated = models.DateField()


class InitiateComplianceRequest(models.Model):
    home_location = models.ForeignKey(Location, related_name='initiate_compliance_requests_home', on_delete=models.CASCADE)
    host_location = models.ForeignKey(Location, related_name='initiate_compliance_requests_host', on_delete=models.CASCADE)
    travel_dates = models.ForeignKey(TravelDate, on_delete=models.CASCADE)
    nationality = models.CharField(max_length=255)
    passport = models.ForeignKey(Passport, on_delete=models.CASCADE)
    trip_details = models.ForeignKey(TripDetail, on_delete=models.CASCADE)
    compliance_types = models.CharField(max_length=255, choices=[("PWN", "PWN"), ("SS", "SS"), ("BV", "BV")])


class InitiateComplianceResponse(models.Model):
    status = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    compliance_request_id = models.CharField(max_length=255)
    compliance_types = models.JSONField()
    next_step_api_endpoint = models.URLField()
    next_step_http_method = models.CharField(max_length=255)
    next_step_request_body = models.JSONField()
    government_portal_data = models.ForeignKey(GovernmentPortalData, on_delete=models.CASCADE)


class FormFieldsComplianceResponse(models.Model):
    status = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    compliance_type = models.JSONField()
    required_fields_pwn = models.ForeignKey(PWNField, related_name='required_fields_pwn', on_delete=models.CASCADE)
    required_fields_ss = models.ForeignKey(SSField, related_name='required_fields_ss', on_delete=models.CASCADE)
    required_fields_bv = models.ForeignKey(BVField, related_name='required_fields_bv', on_delete=models.CASCADE)


class SubmitComplianceRequest(models.Model):
    compliance_request_id = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    compliance_types = models.JSONField()
    government_portal_data = models.ForeignKey(GovernmentPortalData, on_delete=models.CASCADE)


class SubmitComplianceResponse(models.Model):
    status = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    compliance_request_id = models.CharField(max_length=255)
    government_portal_data = models.ForeignKey(GovernmentPortalData, on_delete=models.CASCADE)


class ComplianceRequestsResponse(models.Model):
    status = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    total_results = models.IntegerField()
    page_size = models.IntegerField()
    page_number = models.IntegerField()
    requests = models.ManyToManyField(Request)


class ComplianceRequestResponse(models.Model):
    status = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    data = models.ForeignKey(Request, on_delete=models.CASCADE)