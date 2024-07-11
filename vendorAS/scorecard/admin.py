from django.contrib import admin
from .models import Vendor, PerformanceArea, ScoreCriteria, Appraisal, Report, AuditTrail, Department, Role, UserProfile, SupplierScorecard, BTSOSAdmin, BackOfficeAdmin, FrontOfficerUser, ReportViewer

class SuplierScorecardAdmin(admin.ModelAdmin):
    list_display = ('supplier_name', 'contract', 'overall_rating', 'review_date')
# Register your models here.
admin.site.register(Vendor)
admin.site.register(PerformanceArea)
admin.site.register(ScoreCriteria)
admin.site.register(Appraisal)
admin.site.register(Report)
admin.site.register(AuditTrail)
admin.site.register(Department)
admin.site.register(Role)
admin.site.register(UserProfile)
admin.site.register(SupplierScorecard)
admin.site.register(BTSOSAdmin)
admin.site.register(BackOfficeAdmin)
admin.site.register(FrontOfficerUser)
admin.site.register(ReportViewer)