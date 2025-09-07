from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Event, TeamMember, ContactMessage

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'date', 'is_past_event')
    list_filter = ('event_type', 'is_past_event')
    search_fields = ('title', 'description')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'year_range', 'department')
    list_filter = ('category',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'timestamp', 'is_resolved')
    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        queryset.update(is_resolved=True)