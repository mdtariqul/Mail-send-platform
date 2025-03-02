from django.db import models

class EmailTask(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Sent', 'Sent'),
        ('Failed', 'Failed'),
    ]

    subject = models.CharField(max_length=255)
    message = models.TextField()
    recipient = models.EmailField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
