from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from .models import User, Events, RSVP
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

import random
import json


#Generates a unique id for each listing to avoid name conflicts
def generate_id():

    #Iterates through a random id until one that doesnt exits is found
    while True:
                random_id = random.randint(1000, 10000)

                if not Events.objects.filter(id=random_id).exists():
                    return random_id

#Shows user all events hosted or rsvped for if any and user signed in
def index(request):
    user = request.user

    if user.is_authenticated:
        rsvps = RSVP.objects.filter(user=user).order_by('event__RSVP_deadline')
        events = Events.objects.filter(user=user).order_by('RSVP_deadline')
        rsvps = rsvps.reverse()
    else:
        rsvps = RSVP.objects.none()
        events = Events.objects.none()


    return render(request, 'event/index.html', {
        'rsvps': rsvps,
        'events': events,
    })

#Displays all the events ordered by deadline date/time that are not expired
def calendar(request):

    now = timezone.now()

    events = Events.objects.filter(RSVP_deadline__gte=now).order_by('RSVP_deadline')

    return render(request, 'event/calendar.html', {
        'events': events,
    })

@login_required
#Allows user to rsvp for an event if logged in
def rsvp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            event_id = data.get('event_id')

            event = get_object_or_404(Events, id=event_id)

            #Creates a new rsvp if it doesnt already exist
            if not RSVP.objects.filter(user=user, event=event).exists():
                rsvp_object = RSVP.objects.create(user=user, event=event)
                rsvp_object.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'RSVP already exists'})
        except:
            return JsonResponse({'sucess': False, 'error': 'invalid data or error in data'})
        
    #Handles errors if invalid or event doesn't exist
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)    


#Displays the selected event based on the event id if event exists
def event(request, event_id=None):
   
    if event_id:
        user = request.user
        event = Events.objects.get(id=event_id)
        if user.is_authenticated:
            ticket_exists = RSVP.objects.filter(user=user, event=event).exists()
        else:
            ticket_exists = False
                
        event_object = get_object_or_404(Events, id=event_id)
             
        can_rsvp = event.RSVP_deadline and event.RSVP_deadline > timezone.now()
        return render(request, 'event/event.html', {
            "event": event_object,
            "ticket_exists":ticket_exists,
            "can_rsvp": can_rsvp
        })
    else:
        return render(request, 'event/index.html')


@csrf_exempt
#Loads several categories which have event listeners and sends a fetch request to then list the events of the selected category
def discover(request):

    if request.method == 'POST':

        category = json.loads(request.body).get('category')
        

        event_objects = list(Events.objects.filter(category=category).values())
        
        return JsonResponse({'events': event_objects})

    return render(request, 'event/discover.html', {
        'categories': Events.category.field.choices
    })

#For creating the rsvp from a form submitted by the user
def create(request):
    if request.method == "POST":
        
        #Variables to create an object with based on the event model
        username = request.user
        title = request.POST.get("title") or "Untitled"
        description = request.POST.get("description") or "No description"
        category = request.POST.get("category_field") or "unlisted"
        start_date = request.POST.get("start_date")
        start_time = request.POST.get("start_time")
        end_date = request.POST.get("end_date")
        end_time = request.POST.get("end_time")
        capacity = request.POST.get("capacity")
        ticket_price = request.POST.get("ticket_price")
        RSVP_deadline = request.POST.get("RSVP_deadline")


        try:

            if RSVP_deadline:
                rsvp_datetime = datetime.strptime(RSVP_deadline, '%Y-%m-%dT%H:%M')
                rsvp_datetime = timezone.make_aware(rsvp_datetime) 

            start_datetime = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(), 
                                               datetime.strptime(start_time, '%H:%M').time())
            start_datetime = timezone.make_aware(start_datetime)
            
            end_datetime = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),
                                             datetime.strptime(end_time, '%H:%M').time())
            end_datetime = timezone.make_aware(end_datetime)

            event_object = Events.objects.create(
                user=username,
                title=title,
                description=description,
                category=category,
                start_date=start_datetime,
                start_time=start_datetime.time(),
                end_date=end_datetime,
                end_time=end_datetime.time(),
                capacity=capacity,
                ticket_price=ticket_price,
                RSVP_deadline=rsvp_datetime,
                id = generate_id()
            )
            
            return HttpResponseRedirect(reverse(index))
        
        except Exception as err:
            print(err)
            return render(request, 'event/create.html')

    else:
        categories = Events._meta.get_field('category').choices
        return render(request, 'event/create.html', {'categories': categories})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'event/login.html',{
                "message": "Invalid email or password"
            })
    else:
        return render(request, 'event/login.html')

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if User.objects.filter(username=username).exists():
            return render(request, 'event/register.html', {
                "message": "username already taken"
            })
        elif password != password2:
            return render(request, 'event/register.html', {
                "message": "passwords must match"
            })
        try:
            user_object = User.objects.create_user(username=username, password=password)
            user_object.save()
        except Exception as err:
            print(err)
            return render(request, 'event/register.html', {
                "message": "An error was encountered"
            })
        login(request, user_object)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'event/register.html')

