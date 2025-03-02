from celery import shared_task
from django.core.mail import send_mail
from .models import EmailTask
import time

@shared_task
def process_email_tasks():
    # Fetch up to 100 pending email tasks
    start_time = time.time()
    pending_tasks = EmailTask.objects.filter(status='Pending')[:100]
    #print(f"Method completed in  seconds")
 

    for task in pending_tasks:
        try:
            # Mark as processing
            task.status = 'Processing'
            task.save()

            # Send the email
            send_mail(
                subject=task.subject,
                message=task.message,
                from_email='tariquli241@gmail.com',
                recipient_list=[task.recipient],
                auth_user='tariquli241@gmail.com',
                auth_password='mdqi srrx yjob flgw'  # Replace with your app password
            )

            # Update task status to sent
            task.status = 'Sent'
        except Exception as e:
            # Update task status to failed and log the error
            task.status = 'Failed'
            task.error_message = str(e)
        finally:
            task.save()

    end_time = time.time()
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Method completed in {elapsed_time:.6f} seconds")




