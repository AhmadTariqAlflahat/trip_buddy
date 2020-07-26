from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Trip
import bcrypt


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        error = User.objects.validate(request)

        if error:
            return redirect('/')

        hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        decoded_hash = hashed.decode('utf-8')

        user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=decoded_hash
        )

        request.session['id'] = user.id
        return redirect('/dashboard/')

def login(request):
    if request.method == 'POST':
        error = User.objects.validate_login(request)
        if error:
            return redirect('/')

        return redirect('/dashboard/')


def dashboard(request):
    if 'id' not in request.session:
        return redirect('/')
    user_id = request.session['id']
    print(user_id)
    context = {
        'user': User.objects.get(id=user_id),
        'my_trips': Trip.objects.filter(planner_id=user_id).order_by('start_date'),
        'join_trips': Trip.objects.filter(travelers=user_id).order_by('start_date'),
        'all_other_trips': Trip.objects.exclude(planner_id=user_id).exclude(travelers=user_id).order_by('start_date')
    }
    return render(request, 'dashboard.html', context)
    

def new_trip(request):
    if 'id' not in request.session:
            return redirect('/')

    user = User.objects.get(id=request.session['id'])
    if request.method == 'POST':
        error = Trip.objects.validation(request)

        if error:
            return redirect('/new-trip/')
        
        trip = Trip.objects.create(
            planner=user,
            destination=request.POST['destination'],
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            plan=request.POST['plan'],
        )
        return redirect('/dashboard/')
    
    context = {
        'user': user
    }
    return render(request, 'new.html', context)


def remove(request, id):
    if 'id' not in request.session:
        return redirect('/')
    
    user = User.objects.get(id=request.session['id'])
    trip = Trip.objects.get(id=id)

    if user == trip.planner:
        trip.delete()
    else:
        messages.error(request, 'You can delete this trip, due to that you are not the owner of it.')
    
    return redirect('/dashboard/')
    
def edit_trip(request, id):
    if 'id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    trip = Trip.objects.get(id=id)

    if request.method == 'POST':
        error = Trip.objects.validation(request)

        if error:
            return redirect('/edit-trip/', id=id)

        trip.destination=request.POST['destination']
        trip.destination=request.POST['start_date']
        trip.destination=request.POST['end_date']
        trip.destination=request.POST['plan']
        trip.save()
        return redirect('/dashboard/')
        

    context = {
        'user':user,
        'trip':trip
    }
    if user == trip.planner:
        return render(request, 'edit.html', context)
    else:
        messages.error(request, 'You can edit this trip, due to that you are not the owner of it.')
        return redirect('/dashboard/')


def detail(request, id):
    if 'id' not in request.session:
        return redirect('/')

    context = {
        'user':User.objects.get(id=request.session['id']),
        'trip':Trip.objects.get(id=id),
        'people':Trip.objects.filter(travelers=id),
    }
    return render(request, 'view_trip.html', context)


def join(request, id):
    if 'id' not in request.session:
        return redirect('/')
    
    Trip.objects.get(id=id).travelers.add(request.session['id'])
    return redirect('/dashboard/')


def cancel(request, id):
    if 'id' not in request.session:
        return redirect('/')
    
    Trip.objects.get(id=id).travelers.remove(request.session['id'])
    return redirect('/dashboard/')

def logout(request):
    request.session.clear()
    return redirect('/')