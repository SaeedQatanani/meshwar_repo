from django.contrib import messages
from django.shortcuts import redirect, render
from .models import City, Activity
from login_app.models import User
import random

#function for '' route
def dashboard(request):
    try:
        logged_user = User.objects.get(id = request.session['id'])
        context = {
            "all_cities": City.objects.all(),
        }
        return render(request, 'dashboard.html', context)
    except:
        return redirect('/')

#function for '<int:city_id>/' route
def city_dashboard(request, city_id):
    try:
        logged_user = User.objects.get(id = request.session['id'])
        context = {
            "all_cities": City.objects.all(),
            "city": City.objects.get(id=city_id),
            "city_activities": City.objects.get(id=city_id).activities.all().order_by('-updated_at'),
        }
        return render(request, 'city_dashboard.html', context)
    except:
        return redirect('/')
    

#function for 'profile/<int:user_id>/' route
def show_profile(request, user_id):
    try:
        logged_user = User.objects.get(id = request.session['id'])
        context = {
            'all_cities' : City.objects.all(),
            'user_activities': logged_user.activities_added.all().order_by('-updated_at'),
            'user': logged_user,
            'liked_activities': logged_user.liked_activities.all().order_by('-updated_at'), 
        }
        if logged_user.id == user_id:
            return render(request, 'profile.html', context)
        else:
            return redirect('/dashboard')
    except:
        return redirect('/')

#function for 'new/' route
def new_activity(request):
    try:
        logged_user = User.objects.get(id = request.session['id'])
        context = {
            'all_cities' : City.objects.all(),
        }
        return render(request, 'new_activity.html', context)
    except:
        return redirect('/')

#function for 'show/<int:activity_id>/' route
def show_activity(request, activity_id):
    try:
        logged_user = User.objects.get(id = request.session['id'])
        context ={
            'activity' : Activity.objects.get(id = activity_id),
            'all_cities' : City.objects.all(),
            'user' : logged_user,
        }
        return render(request, 'show_activity.html', context)
    except:
        return redirect('/')

#function for 'edit/<int:activity_id>/' route
def edit_activity(request, activity_id):
    try:
        logged_user = User.objects.get(id = request.session['id'])
        if logged_user.id == Activity.objects.get(id=activity_id).added_by.id:
            if Activity.objects.get(id=activity_id).start_date:
                context = {
                    "all_cities" : City.objects.all(),
                    "activity": Activity.objects.get(id=activity_id),
                    "activity_start_date": Activity.objects.get(id=activity_id).start_date.strftime('%Y-%m-%d %H:%M:%S'),
                    "activity_end_date": Activity.objects.get(id=activity_id).end_date.strftime('%Y-%m-%d %H:%M:%S'),
                }
            else:
                context = {
                    "all_cities" : City.objects.all(),
                    "activity": Activity.objects.get(id=activity_id),
                }
            return render(request, 'edit_activity.html', context)
        else:
            return redirect('/dashboard')
    except:
        return redirect('/')

#function for 'update/<int:activity_id>/' route
def update_activity(request, activity_id):
    errors = Activity.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/dashboard/edit/{activity_id}')
    else:
        user = User.objects.filter(id = request.session['id'])
        logged_user = user[0]
        activity_to_update = Activity.objects.get(id = activity_id)
        activity_city = City.objects.get(id = int(request.POST['city']))
        if logged_user.id == activity_to_update.added_by.id:
            activity_to_update.title = request.POST['title']
            activity_to_update.location = request.POST['location']
            activity_to_update.desc = request.POST['description']
            activity_to_update.price = request.POST['price']
            activity_to_update.city = activity_city
            if request.POST['start_date']:
                activity_to_update.start_date = request.POST['start_date']
                activity_to_update.end_date = request.POST['end_date']
            activity_to_update.save()
            return redirect(f'/dashboard/show/{activity_id}')
        else:
            return redirect('/dashboard/')

#function for 'about/' route
#This function renders an HTML template containing information about the site and its founders.
def about_us(request):
    context = {
        'all_cities' : City.objects.all(),
    }
    return render(request, 'about_us.html', context)

#function for 'create/' route
def create_activity(request):
    errors = Activity.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/dashboard/new')
    else:
        user = User.objects.filter(id = request.session['id'])
        if user: 
            logged_user = user[0]
            activity_city = City.objects.get(id = int(request.POST['city']))
            if request.POST['start_date']:
                new_activity = Activity.objects.create(title = request.POST['title'],
                            location = request.POST['location'],
                            start_date = request.POST['start_date'],
                            end_date = request.POST['end_date'],
                            desc = request.POST['description'],
                            price = request.POST['price'],
                            added_by = logged_user,
                            city = activity_city,
                            )
            else:
                new_activity = Activity.objects.create(title = request.POST['title'],
                            location = request.POST['location'],
                            desc = request.POST['description'],
                            price = request.POST['price'],
                            added_by = logged_user,
                            city = activity_city,
                            )
        return redirect(f'/dashboard/show/{new_activity.id}')

#function for 'delete/<int:activity_id>/' route
def delete_activity(request, activity_id):
    try:
        logged_user = User.objects.get(id = request.session['id'])
        activity_to_delete = Activity.objects.get(id = activity_id)
        if logged_user.id == activity_to_delete.added_by.id:
            activity_to_delete.delete()
            return redirect(f'/dashboard/profile/{logged_user.id}')
        else:
            return redirect('/dashboard')
    except:
        return redirect('/')

#function for 'like_activity/<int:activity_id>/' route
#This function adds an activity to the user's list of liked activities when 'vote up' button is clicked 
def like_activity(request, activity_id):
    try:
        logged_user = User.objects.get(id = request.session['id'])
        liked_activity = Activity.objects.get(id = activity_id)
        if liked_activity in logged_user.liked_activities.all():
            logged_user.liked_activities.remove(liked_activity)
        else:
            logged_user.liked_activities.add(liked_activity)
        if liked_activity in logged_user.disliked_activities.all():
            logged_user.disliked_activities.remove(liked_activity)
        return redirect(f'/dashboard/show/{liked_activity.id}')
    except:
        return redirect('/')

#function for 'dislike_activity/<int:activity_id>/' route
#This function adds an activity to the user's list of disliked activities when 'vote down' button is clicked 
def dislike_activity(request, activity_id):
    try:
        logged_user = User.objects.get(id = request.session['id'])
        disliked_activity = Activity.objects.get(id = activity_id)
        if disliked_activity in logged_user.disliked_activities.all():
            logged_user.disliked_activities.remove(disliked_activity)
        else:
            logged_user.disliked_activities.add(disliked_activity)
        if disliked_activity in logged_user.liked_activities.all():
            logged_user.liked_activities.remove(disliked_activity)
        return redirect(f'/dashboard/show/{disliked_activity.id}')
    except:
        return redirect('/')

#function for 'random/' route
def show_random(request):
    try:
        request.session['random_activity_id']
        context = {
                "all_cities" : City.objects.all(),
                "random_activity" : Activity.objects.get(id = request.session['random_activity_id']),
            }
    except:
        context = {
                    "all_cities" : City.objects.all(),
                }
    return render(request, 'random.html', context)

#function for 'random/get/' route
#This function chooses a random activity in a user chosen city.
def pick_random(request):
    city_id = int(request.POST['city'])
    activities = City.objects.get(id =city_id).activities.all()
    try:
        random_activity= random.choice(activities)
        request.session['random_activity_id'] = random_activity.id
        return redirect('/dashboard/random')
    except:
        try:
            del request.session['random_activity_id']
            return redirect('/dashboard/random')
        except:
            return redirect('/dashboard/random')

#Admin functions to create a city
def add_city(request):
    return render(request, 'create_city.html')

def create_city(request):
    City.objects.create(name = request.POST['city'])
    return redirect('/dashboard/add_city')