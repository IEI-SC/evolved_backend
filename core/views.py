from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Event, TeamMember
from .forms import ContactForm

def home(request):
    upcoming_events = Event.objects.filter(is_past_event=False).order_by('date')[:3]
    past_events = Event.objects.filter(is_past_event=True).order_by('-date')[:3]
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'core/home.html', context)

def event_list(request):
    event_type = request.GET.get('type', None)
    events = Event.objects.all().order_by('-date')
    
    if event_type:
        events = events.filter(event_type=event_type)
    
    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/events.html', {
        'page_obj': page_obj,
        'event_types': Event.EVENT_TYPES
    })

@api_view(['GET'])
def team_view(request):
    category = request.GET.get('category', None)
    faculty = TeamMember.objects.filter(category='faculty').order_by('designation')
    
    students = {
        'convenors': TeamMember.objects.filter(category='convenor').order_by('designation'),
        'committee': TeamMember.objects.filter(category='committee').order_by('designation'),
        'members': TeamMember.objects.filter(category='member').order_by('designation'),
        'tech': TeamMember.objects.filter(category='tech').order_by('designation'),
        'graphics': TeamMember.objects.filter(category='graphics').order_by('designation'),
        'pr': TeamMember.objects.filter(category='pr').order_by('designation'),
        'manage': TeamMember.objects.filter(category='manage').order_by('designation')
    }
    
    return render(request, 'core/team.html', {
        'faculty': faculty,
        'students': students
    })

# API endpoint for team members
@api_view(['GET'])
def api_team_members(request):
    category = request.GET.get('category', None)
    
    if category:
        # Map frontend category names to database values
        category_mapping = {
            'faculty': 'faculty',
            'conveners': 'convenor',
            'committee': 'committee',
            'members': 'member',
            'tech': 'tech',
            'graphics': 'graphics',
            'pr': 'pr',
            'management': 'manage'
        }
        
        db_category = category_mapping.get(category)
        if db_category:
            members = TeamMember.objects.filter(category=db_category).order_by('designation')
        else:
            members = TeamMember.objects.none()
    else:
        members = TeamMember.objects.all().order_by('designation')
    
    data = [
        {
            'id': member.id,
            'name': member.name,
            'role': member.designation,
            'imageUrl': member.image.url if member.image else None,
            'category': member.category,
            'linkedin': member.linkedin,  # Add this line
            'instagram': member.instagram,  # Add this line
            'department': member.department,
        }
        for member in members
    ]
    
    return Response(data)

# Structured API endpoint for all team data
# In views.py
@api_view(['GET'])
def api_team_structured(request):
    faculty = TeamMember.objects.filter(category='faculty').order_by('designation')
    
    students = {
        'convenors': TeamMember.objects.filter(category='convenor').order_by('designation'),
        'committee': TeamMember.objects.filter(category='committee').order_by('designation'),
        'members': TeamMember.objects.filter(category='member').order_by('designation'),
        'tech': TeamMember.objects.filter(category='tech').order_by('designation'),
        'graphics': TeamMember.objects.filter(category='graphics').order_by('designation'),
        'pr': TeamMember.objects.filter(category='pr').order_by('designation'),
        'manage': TeamMember.objects.filter(category='manage').order_by('designation')
    }
    
    def serialize_members(members):
        return [
            {
                'id': member.id,
                'name': member.name,
                'role': member.designation,
                'imageUrl': member.image.url if member.image else None,
                'category': member.category,
                'linkedin': member.linkedin,  # Add this line
                'instagram': member.instagram,  # Add this line
                'department': member.department,  # Optional: if you want to show department
            }
            for member in members
        ]
    
    data = {
        'faculty': serialize_members(faculty),
        'students': {
            'convenors': serialize_members(students['convenors']),
            'committee': serialize_members(students['committee']),
            'members': serialize_members(students['members']),
            'tech': serialize_members(students['tech']),
            'graphics': serialize_members(students['graphics']),
            'pr': serialize_members(students['pr']),
            'manage': serialize_members(students['manage'])
        }
    }
    
    return Response(data)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'core/event_detail.html', {'event': event})

def contact_success(request):
    return render(request, 'core/contact_success.html')

def about(request):
    return render(request, 'core/about.html')







from rest_framework import viewsets
from .models import Event, TeamMember
from .serializers import EventSerializer, TeamMemberSerializer

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all().order_by('-date')
    serializer_class = EventSerializer

class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer

def team_data_api(request):
    faculty = TeamMember.objects.filter(category='faculty').order_by('designation')
    students = {
        'convenors': TeamMember.objects.filter(category='convenor').order_by('designation'),
        'committee': TeamMember.objects.filter(category='committee').order_by('designation'),
        'members': TeamMember.objects.filter(category='member').order_by('designation'),
        'tech': TeamMember.objects.filter(category='tech').order_by('designation'),
        'graphics': TeamMember.objects.filter(category='graphics').order_by('designation'),
        'pr': TeamMember.objects.filter(category='pr').order_by('designation'),
        'manage': TeamMember.objects.filter(category='manage').order_by('designation')
    }
    
    # You'll need to create a proper serializer for this or return JSON response
    from django.http import JsonResponse
    data = {
        'faculty': list(faculty.values()),
        'students': {key: list(qs.values()) for key, qs in students.items()}
    }
    return JsonResponse(data)




    # In views.py, add this API endpoint
@api_view(['GET'])
def api_events(request):
    event_type = request.GET.get('type', None)
    is_past = request.GET.get('past', None)
    
    events = Event.objects.all().order_by('-date')
    
    if event_type:
        events = events.filter(event_type=event_type)
    
    if is_past is not None:
        if is_past.lower() == 'true':
            events = events.filter(is_past_event=True)
        elif is_past.lower() == 'false':
            events = events.filter(is_past_event=False)
    
    data = [
        {
            'id': event.id,
            'title': event.title,
            'event_type': event.event_type,
            'date': event.date.strftime('%Y-%m-%d %H:%M:%S'),
            'description': event.description,
            'registration_link': event.registration_link,
            'is_past_event': event.is_past_event,
            'imageUrl': event.thumbnail.url if event.thumbnail else None,  # Changed to imageUrl
        }
        for event in events
    ]
    
    return Response(data)