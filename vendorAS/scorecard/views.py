from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from .forms import PerformanceAreaForm, ScoreCriteriaForm, VendorForm, AppraisalForm, ReportForm, UserForm, RoleForm, SupplierScorecardForm, AuditTrailForm, DateRangeForm, RatingScaleForm
from .models import PerformanceArea, ScoreCriteria, Vendor, Appraisal, Report, Role, SupplierScorecard, User, UserProfile, AuditTrail, RatingScale
import csv
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def home(request):
    return render(request, 'home.html')

@login_required
def performance_area_list(request):
    performance_areas = PerformanceArea.objects.all()
    return render(request, 'performance_area_list.html', {'performance_areas': performance_areas})

@login_required
def performance_area_create(request):
    if request.method == 'POST':
        form = PerformanceAreaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('performance_area_list')
    else:
        form = PerformanceAreaForm()
    return render(request, 'performance_area_form.html', {'form': form})

@login_required
def performance_area_edit(request, pk):
    performance_area = get_object_or_404(PerformanceArea, pk=pk)
    if request.method == 'POST':
        form = PerformanceAreaForm(request.POST, instance=performance_area)
        if form.is_valid():
            form.save()
            return redirect('performance_area_list')
    else:
        form = PerformanceAreaForm(instance=performance_area)
    return render(request, 'performance_area_form.html', {'form': form})

@login_required
def performance_area_delete(request, pk):
    performance_area = get_object_or_404(PerformanceArea, pk=pk)
    if request.method == 'POST':
        performance_area.delete()
        return redirect('performance_area_list')
    return render(request, 'performance_area_confirm_delete.html', {'performance_area': performance_area})

@login_required
def score_criteria_list(request):
    score_criteria = ScoreCriteria.objects.all()
    return render(request, 'score_criteria_list.html', {'score_criteria': score_criteria})

@login_required
def score_criteria_create(request):
    if request.method == 'POST':
        form = ScoreCriteriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('score_criteria_list')
    else:
        form = ScoreCriteriaForm()
    return render(request, 'score_criteria_form.html', {'form': form})

@login_required
def score_criteria_edit(request, pk):
    score_criteria = get_object_or_404(ScoreCriteria, pk=pk)
    if request.method == 'POST':
        form = ScoreCriteriaForm(request.POST, instance=score_criteria)
        if form.is_valid():
            form.save()
            return redirect('score_criteria_list')
    else:
        form = ScoreCriteriaForm(instance=score_criteria)
    return render(request, 'score_criteria_form.html', {'form': form})

@login_required
def score_criteria_delete(request, pk):
    score_criteria = get_object_or_404(ScoreCriteria, pk=pk)
    if request.method == 'POST':
        score_criteria.delete()
        return redirect('score_criteria_list')
    return render(request, 'score_criteria_confirm_delete.html', {'score_criteria': score_criteria})

@login_required
def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor_list.html', {'vendors': vendors})

@login_required
def vendor_create(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vendor_list')
    else:
        form = VendorForm()
    return render(request, 'vendor_form.html', {'form': form})

@login_required
def vendor_edit(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('vendor_list')
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'vendor_form.html', {'form': form})

@login_required
def vendor_delete(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        vendor.delete()
        return redirect('vendor_list')
    return render(request, 'vendor_confirm_delete.html', {'vendor': vendor})

@login_required
def appraisal_list(request):
    appraisals = Appraisal.objects.all()
    for appraisal in appraisals:
        appraisal.weighted_rating = appraisal.performance_score * appraisal.score_criteria.weight
    return render(request, 'appraisal_list.html', {'appraisals': appraisals})
    
@login_required
def appraisal_create(request):
    if request.method == 'POST':
        form = AppraisalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appraisal_list')
    else:
        form = AppraisalForm()
    return render(request, 'appraisal_form.html', {'form': form})

@login_required
def appraisal_edit(request, pk):
    appraisal = get_object_or_404(Appraisal, pk=pk)
    if request.method == 'POST':
        form = AppraisalForm(request.POST, instance=appraisal)
        if form.is_valid():
            form.save()
            return redirect('appraisal_list')
    else:
        form = AppraisalForm(instance=appraisal)
    return render(request, 'appraisal_form.html', {'form': form})

@login_required
def appraisal_delete(request, pk):
    appraisal = get_object_or_404(Appraisal, pk=pk)
    if request.method == 'POST':
        appraisal.delete()
        return redirect('appraisal_list')
    return render(request, 'appraisal_confirm_delete.html', {'appraisal': appraisal})


@login_required
def report_list(request):
    reports = Report.objects.all()
    if request.method == 'GET':
        form = DateRangeForm(request.GET)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            if start_date and end_date:
                reports = reports.filter(created_at__range=(start_date, end_date))
    else:
        form = DateRangeForm()
    return render(request, 'report_list.html', {'reports': reports, 'form': form})

@login_required
def download_csv(request):
    reports = Report.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reports.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Description', 'Appraisal', 'Backoffice Admin'])
    for report in reports:
        writer.writerow([report.description, report.appraisal, report.backoffice_admin])
    
    return response

@login_required
def download_pdf(request):
    reports = Report.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    y = height - 50

    p.drawString(100, y, 'Description')
    p.drawString(300, y, 'Appraisal')
    p.drawString(500, y, 'Backoffice Admin')
    y -= 20

    for report in reports:
        p.drawString(100, y, report.description)
        p.drawString(300, y, str(report.appraisal))
        p.drawString(500, y, str(report.backoffice_admin))
        y -= 20

    p.showPage()
    p.save()

    return response

@login_required
def report_create(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('report_list')
    else:
        form = ReportForm()
    return render(request, 'report_form.html', {'form': form})

@login_required
def report_edit(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('report_list')
    else:
        form = ReportForm(instance=report)
    return render(request, 'report_form.html', {'form': form})

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

@login_required
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form})

@login_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        user_profile = UserProfile.objects.get(user=user)
        form = UserForm(instance=user, initial={'role': user_profile.role})
    return render(request, 'user_form.html', {'form': form})

@login_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user_confirm_delete.html', {'user': user})

@login_required
def user_role_list(request):
    roles = Role.objects.all()
    return render(request, 'user_role_list.html', {'roles': roles})

@login_required
def user_role_create(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_role_list')
    else:
        form = RoleForm()
    return render(request, 'user_role_form.html', {'form': form})

@login_required
def user_role_edit(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('user_role_list')
    else:
        form = RoleForm(instance=role)
    return render(request, 'user_role_form.html', {'form': form})

@login_required
def user_role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        role.delete()
        return redirect('user_role_list')
    return render(request, 'user_role_confirm_delete.html', {'role': role})

@login_required
def submit_scorecard(request):
    if request.method == 'POST':
        form = SupplierScorecardForm(request.POST)
        if form.is_valid():
            scorecard = form.save(commit=False)
            scorecard.user = request.user
            scorecard.save()
            return redirect('scorecard_list')
    else:
        form = SupplierScorecardForm()
    return render(request, 'submit_scorecard.html', {'form': form})

@login_required
def scorecard_list(request):
    scorecards = SupplierScorecard.objects.filter(user=request.user)
    return render(request, 'scorecard_list.html', {'scorecards': scorecards})

@login_required
def audit_report_list(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        audits = AuditTrail.objects.filter(timestamp__range=(start_date, end_date))
    else:
        audits = AuditTrail.objects.all()

    return render(request, 'audit_report_list.html', {'audits': audits})

@login_required
def download_audit_csv(request):
    audits = AuditTrail.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="audit_reports.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['User', 'IP Address', 'Device Name', 'Browser Type', 'Action', 'Timestamp'])
    for audit in audits:
        writer.writerow([audit.user.username, audit.ip_address, audit.user_agent, audit.action, audit.timestamp])
    
    return response

@login_required
def download_audit_pdf(request):
    audits = AuditTrail.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="audit_reports.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    y = height - 50

    p.drawString(50, y, 'User')
    p.drawString(150, y, 'IP Address')
    p.drawString(250, y, 'Device Name')
    p.drawString(350, y, 'Browser Type')
    p.drawString(450, y, 'Action')
    p.drawString(550, y, 'Timestamp')
    y -= 20

    for audit in audits:
        p.drawString(50, y, audit.user.username)
        p.drawString(150, y, audit.ip_address)
        p.drawString(250, y, audit.user_agent)
        p.drawString(350, y, audit.action)
        p.drawString(450, y, str(audit.timestamp))
        y -= 20

    p.showPage()
    p.save()

    return response

@login_required
def rating_scale_list(request):
    scales = RatingScale.objects.all()
    return render(request, 'rating_scale_list.html', {'scales': scales})

@login_required
def rating_scale_create(request):
    if request.method == 'POST':
        form = RatingScaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rating_scale_list')
    else:
        form = RatingScaleForm()
    return render(request, 'rating_scale_form.html', {'form': form})

@login_required
def rating_scale_edit(request, pk):
    scale = get_object_or_404(RatingScale, pk=pk)
    if request.method == 'POST':
        form = RatingScaleForm(request.POST, instance=scale)
        if form.is_valid():
            form.save()
            return redirect('rating_scale_list')
    else:
        form = RatingScaleForm(instance=scale)
    return render(request, 'rating_scale_form.html', {'form': form})

@login_required
def rating_scale_delete(request, pk):
    scale = get_object_or_404(RatingScale, pk=pk)
    if request.method == 'POST':
        scale.delete()
        return redirect('rating_scale_list')
    return render(request, 'rating_scale_confirm_delete.html', {'scale': scale})
