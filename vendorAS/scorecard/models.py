from django.db import models
from django.contrib.auth.models import User,Permission

class AuditTrail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.action}'

class Department(models.Model):
    department_name = models.CharField(max_length=255)
 
    def __str__(self):
        return self.department_name

class Role(models.Model):
    role_name = models.CharField(max_length=255)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.role_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

class BTSOSAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

class BackOfficeAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

class FrontOfficerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

class ReportViewer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

class Vendor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    industry = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=255)
    tax_identification_number = models.CharField(max_length=255)
    years_in_business = models.IntegerField()
    production_capacity = models.CharField(max_length=255)
    product_types = models.CharField(max_length=255)
    service_types = models.CharField(max_length=255)
    frontend_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='vendors')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class PerformanceArea(models.Model):
    area_name = models.CharField(max_length=255)
    description = models.TextField()
    percentage_weight = models.FloatField()

    def __str__(self):
        return self.area_name

class ScoreCriteria(models.Model):
    criteria_description = models.CharField(max_length=255)
    weight = models.FloatField()
    performance_area = models.ForeignKey(PerformanceArea, on_delete=models.CASCADE)

    def __str__(self):
        return self.criteria_description

class RatingScale(models.Model):
    value = models.IntegerField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.value} - {self.description}'

class Appraisal(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    frontend_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='appraisals')
    score_criteria = models.ForeignKey(ScoreCriteria, on_delete=models.CASCADE)
    performance_score = models.FloatField()
    #rating_scale = models.ForeignKey(RatingScale, on_delete=models.CASCADE, default=RatingScale.objects.get(value=1).id)
    rating_scale = models.ForeignKey(RatingScale, on_delete=models.CASCADE, default=1)
    comments = models.TextField(null=True, blank=True)
    area_weight = models.FloatField(default=0)
    area_rating = models.FloatField(default=0)
    wtd_rating = models.FloatField(default=0)

    def __str__(self):
        return f'{self.vendor} - {self.performance_score}'


class Report(models.Model):
    description = models.TextField()
    backoffice_admin = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reports')
    appraisal = models.ForeignKey(Appraisal, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
    
class SupplierScorecard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    supplier_name = models.CharField(max_length=255)
    contract = models.CharField(max_length=255)
    product_service_name = models.CharField(max_length=255)
    total_period_use = models.IntegerField()
    overall_rating = models.FloatField()
    review_date = models.DateField()

    def __str__(self):
        return self.supplier_name
    