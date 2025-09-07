from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify
class Event(models.Model):
    EVENT_TYPES = [
        ('workshop', 'Workshop'),
        ('lecture', 'Guest Lecture'),
        ('competition', 'Competition'),
    ]
    
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    date = models.DateTimeField()
    description = models.TextField(blank=True)
    registration_link = models.URLField(blank=True)
    is_past_event = models.BooleanField(default=False)
    report_pdf = models.FileField(upload_to='event_reports/', blank=True)
    thumbnail = models.ImageField(upload_to='event_thumbnails/')

    def __str__(self):
        return f"{self.title} ({self.get_event_type_display()})"
    
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class TeamMember(models.Model):
    CATEGORY_CHOICES = [
        ('faculty', 'Faculty'),
        ('convenor', 'Convenor'),
        ('committee', 'Committee'),
        ('member', 'Member'),
        ('tech', 'Tech Team'),
        ('graphics', 'Graphics Team'),
        ('pr', 'PR Team'),
        ('manage', 'Management Team'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null='False')
    designation = models.CharField(max_length=100, null='False', blank=True)  # Custom designation field
    year_range = models.CharField(max_length=20, null='False')  # Format: "2023-2025"
    image = models.ImageField(upload_to='team/')
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    department = models.CharField(max_length=100, blank=True)
    additional_info = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} at {self.timestamp}"