from django.shortcuts import render
from .forms import EmailForm
from .tasks import process_email_tasks
import pandas as pd
from django.core.mail import send_mail
from .models import EmailTask
import re



def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None



def send_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Load email recipients from an Excel file
            #df = pd.read_excel(r'C:\Users\PRO GADGET\Desktop\New folder (2)\Mail_send\mailsend\data\mail_list.xlsx')
            df = pd.read_csv(r'C:\Users\PRO GADGET\Desktop\Mail_send\mailsend\data\Email List - Sheet1.csv')
            recipient_list = df['EMAIL'].drop_duplicates().tolist()
            valid_recipient_list = [email for email in recipient_list if is_valid_email(email)]

            # Save each email task in the database
            for recipient in valid_recipient_list:
                EmailTask.objects.create(subject=subject, message=message, recipient=recipient)



                
            #request.session['email_task_ids'] = task_ids
            process_email_tasks.delay()
            success_message = f"Emails are being sent to {len(valid_recipient_list)} recipients in batches."
            return render(request, 'send_email.html', {'form': form, 'success_message': success_message})
    else:
        form = EmailForm()

    return render(request, 'send_email.html', {'form': form})
