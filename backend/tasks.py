from celery_worker import celery_app
from models import db, Application, User, PlacementDrive
import csv
import os
from datetime import datetime

# 1. User Triggered Async Job
@celery_app.task
def export_student_applications_csv(student_id, user_email):
    # Retrieve all applications for this student
    applications = Application.query.filter_by(student_id=student_id).all()
    
    filename = f"export_{student_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Student ID', 'Company Name', 'Drive Title', 'Application Status', 'Dates'])
        for app in applications:
            writer.writerow([
                app.student_id,
                app.drive.company.name,
                app.drive.job_title,
                app.status,
                app.applied_at.isoformat()
            ])
            
    # In a real app we'd email this file or upload to S3. Here we simulate an alert/email.
    print(f"[ASYNC JOB DONE] CSV Exported for {user_email} at {filepath}")
    return filepath

# 2. Scheduled Job - Daily reminders (G-Chat webhook/Email mock)
@celery_app.task
def daily_deadline_reminders():
    # Find drives whose deadline is exactly tomorrow
    now = datetime.utcnow()
    # Mocking lookup: Drives open
    open_drives = PlacementDrive.query.filter_by(status='approved').all()
    for d in open_drives:
        delta = d.deadline - now
        if 0 < delta.days <= 1:
            print(f"[SCHEDULED JOB Daily] Reminder: Drive '{d.job_title}' by {d.company.name} ends in 1 day!")
            
    return "Daily Reminders Sent"

# 3. Scheduled Job - Monthly Activity Report
@celery_app.task
def monthly_activity_report():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        return "No admin found"
    
    drives_count = PlacementDrive.query.count()
    apps_count = Application.query.count()
    selected_count = Application.query.filter_by(status='selected').count()
    
    html_report = f"""
    <html>
      <body>
         <h2>Monthly Placement Activity Report</h2>
         <p>Total Drives Conducted: {drives_count}</p>
         <p>Total Applications Received: {apps_count}</p>
         <p>Total Students Selected: {selected_count}</p>
      </body>
    </html>
    """
    
    print(f"\n[SCHEDULED JOB Monthly] Report generated and sent to {admin.email}.")
    # print(html_report)
    return "Monthly Report Sent"

# Beat schedule setup
from celery.schedules import crontab
celery_app.conf.beat_schedule = {
    'daily-reminders': {
        'task': 'tasks.daily_deadline_reminders',
        'schedule': crontab(hour=8, minute=0), # Every day at 8 AM
    },
    'monthly-report': {
        'task': 'tasks.monthly_activity_report',
        # Instead of 'schedule': crontab(0, 0, day_of_month='1'), we run it faster for verification
        'schedule': 60.0, # Every 60s
    }
}
