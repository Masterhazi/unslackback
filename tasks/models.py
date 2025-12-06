
from django.db import models

class Task(models.Model):
    CATEGORY_CHOICES = [
        ('do', 'Do'),
        ('schedule', 'Schedule'),
        ('delegate', 'Delegate'),
        ('eliminate', 'Eliminate'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
