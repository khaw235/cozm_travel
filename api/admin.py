from django.contrib import admin

# Register your models here.
from . import models

admin.register(models.BVField)
admin.register(models.ComplianceRequestResponse)
admin.register(models.ComplianceRequestsResponse)
admin.register(models.EmergencyContact)
admin.register(models.Passport)
admin.register(models.Employee)
admin.register(models.Employer)
admin.register(models.FormFieldsComplianceResponse)
admin.register(models.GovernmentPortalData)
admin.register(models.InitiateComplianceRequest)
admin.register(models.InitiateComplianceResponse)
admin.register(models.Location)
admin.register(models.PersonalInformation)
admin.register(models.PWNData)
admin.register(models.PWNField)
admin.register(models.SocialSecurityInfo)
admin.register(models.Request)
admin.register(models.SSData)
admin.register(models.SSField)
admin.register(models.SubmitComplianceRequest)
admin.register(models.SubmitComplianceResponse)
admin.register(models.TravelDate)
admin.register(models.TripDetail)