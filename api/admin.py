from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.BVField)
admin.site.register(models.ComplianceRequestResponse)
admin.site.register(models.ComplianceRequestsResponse)
admin.site.register(models.EmergencyContact)
admin.site.register(models.Passport)
admin.site.register(models.Employee)
admin.site.register(models.Employer)
admin.site.register(models.FormFieldsComplianceResponse)
admin.site.register(models.GovernmentPortalData)
admin.site.register(models.InitiateComplianceRequest)
admin.site.register(models.InitiateComplianceResponse)
admin.site.register(models.Location)
admin.site.register(models.PersonalInformation)
admin.site.register(models.PWNData)
admin.site.register(models.PWNField)
admin.site.register(models.SocialSecurityInfo)
admin.site.register(models.Request)
admin.site.register(models.SSData)
admin.site.register(models.SSField)
admin.site.register(models.SubmitComplianceRequest)
admin.site.register(models.SubmitComplianceResponse)
admin.site.register(models.TravelDate)
admin.site.register(models.TripDetail)