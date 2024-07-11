from django import forms
from django.contrib.auth.models import User
from .models import Vendor, PerformanceArea, ScoreCriteria, Appraisal, Report, Role, SupplierScorecard, UserProfile, AuditTrail, RatingScale

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'

class PerformanceAreaForm(forms.ModelForm):
    class Meta:
        model = PerformanceArea
        fields = '__all__'

class ScoreCriteriaForm(forms.ModelForm):
    class Meta:
        model = ScoreCriteria
        fields = '__all__'

class AppraisalForm(forms.ModelForm):
    class Meta:
        model = Appraisal
        fields = '__all__'

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'role']

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        if commit:
            user.save()
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.role = self.cleaned_data['role']
            user_profile.save()
        return user

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role_name', 'permissions']
        widgets = {
            'permissions': forms.CheckboxSelectMultiple,
        }

class SupplierScorecardForm(forms.ModelForm):
    class Meta:
        model = SupplierScorecard
        fields = ['supplier_name', 'contract', 'product_service_name', 'total_period_use', 'overall_rating', 'review_date']
        
class AuditTrailForm(forms.ModelForm):
    class Meta:
        model = AuditTrail
        fields = ['user', 'action', 'ip_address', 'user_agent']
        
class DateRangeForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    
class RatingScaleForm(forms.ModelForm):
    class Meta:
        model = RatingScale
        fields = ['value', 'description']
