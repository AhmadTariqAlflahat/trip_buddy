from django.db import models
from django.contrib import messages
import bcrypt
import re
from datetime import datetime

EMAIL_CHECK = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate(self, form):
        error = False
        if len(form.POST['email'])==0:
            error = True
            messages.error(form, 'Email cannot be empty!', extra_tags='email')
        if User.objects.filter(email=form.POST['email']).count() > 0:
            error = True
            messages.error(form, 'Account with this Email already exsits.', extra_tags='email')
        if not EMAIL_CHECK.match(form.POST['email']):
            error = True
            messages.error(form, 'Invalid Email Credentials', extra_tags='email')
        if len(form.POST['first_name']) < 2 or len(form.POST['last_name']) < 2:
            error = True
            messages.error(form, 'First/Last name should be at least 2 Char.', extra_tags='FLname')
        if len(form.POST['password']) < 8:
            error = True
            messages.error(form, 'Password Strength with char less than 8 is weak.', extra_tags='password')
        if form.POST['password'] != form.POST['re-password']:
            error = True
            messages.error(form, 'Passwords are not Match.', extra_tags='password')
        return error
    
    def validate_login(self, request):
        error = False
        user = User.objects.filter(email=request.POST['email'])
        if not user:
            messages.error(request, 'Not such an email in database', extra_tags='login')
            error = True
        
        user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['id'] = user.id
            
        else:
            messages.error(request, 'Password does not match any in database', extra_tags='login')
            error = True
        return error


class TripManager(models.Manager):
    def validation(self, request):
        error = False

        if (len(request.POST['destination']) == 0 
        or len(request.POST['plan']) == 0
        or len(request.POST['start_date']) == 0
        or len(request.POST['end_date']) == 0):
            error = True
            messages.error(request, 'All fileds are requeird!')
        else:
            if request.POST['start_date'] != "":
                start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
            if request.POST['end_date'] != "":
                end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d')
            if start_date != None and end_date != None:
                if start_date < datetime.today():
                    error = True
                    messages.error(request, 'Start date should be in future, not in past!')
                if end_date < start_date:
                    error = True
                    messages.error(request, 'End date %s cannot be happened before Start date %s' %(end_date, start_date) )
        return error


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True)
    password =  models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def get_full_name(self):
        return ('%s %s' % (self.first_name, self.last_name)).strip()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    travelers = models.ManyToManyField(User, related_name='trips')
    planner = models.ForeignKey(User, related_name='trip_planner', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()
    
    
