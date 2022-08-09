#from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import School_RegForm, RoomForm, UserForm
from .models import Debtors, School, Debtor_list, School_Post




def index(request):
    return render(request, 'index.html')


def contact_view(request):
    return render(request, 'contact-us.html', {})

def signup_view(request):
    # if request.user.is_authentecated:
    #     return redirect('home')
    if request.method == 'POST':
        form = School_RegForm(request.POST)
        if form.is_valid():
            user = form.save()
            # email = form.cleaned_data.get('email')
            # password = form.cleaned_data.get('password1')
            # user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('dashboard')
        else:
            form = School_RegForm(request.POST)
            return render(request, 'signup.html', {'form': form})
    else:
        form = School_RegForm(request.POST)
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    # if request.user.is_authentecated:
    # return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            form = AuthenticationForm()
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('signin')
    

def current_debtors(request):
    debtors = Debtors.objects.all().order_by('name')
    return render(request, 'current-debtors.html', {'debtors': debtors})





from django.shortcuts import render
from . import models


# Create your views here.

def home(request):
    return render(request, 'index.html')

def enter_debtors(request):
    pass

def debtor_email(request):
    """_summary_
        This is for testing purposes only.
        The school name will be called by User login details
        while the student email will be gotten from the enter-debtors view
        if the page will come as a popup. else, they will be fetched from the models
    """
    page_contents = {
    "school_name" : "Chrisland school",
    "student_email" : "alexjoe2018@gmail.com",
    "student_name" : "Alex Sonia",
    "contend_link" : "Contend this post",
    "duration_owned" : "two",
    "sponsor_name": "Mr Alex Joe",
    }
    return render(request, 'debtor-email.html', {"page_contents":page_contents})


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import School, School_Post, Debtor_list, Debtors, Comment
from school_app.models import Debtor_list


def room(request, pk):
    room = Debtor_list.objects.get(id=pk)
    room_comment = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Comment.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_comment,
               'participants': participants}
    return render(request, 'school_app/feed.html', context)



def school_list(request):
    """This is a school/debtor filter,
        list of schools and
        search bar inclusive
    """
    schools = School.objects.all()
    return render(request, 'static/school-list.html', {'schools': schools})

    
def specific_sch(request):
    """This is for list of
        debtors in a particular school.
        A one to many relationship
    """
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    specific_debtors = Debtor_list.objects.filter(name__icontains=q)
    return render(request, 'static/specific-school.html', {'specific_debtors': specific_debtors})


def feed_page(request):
    """Feed activity: contains school posts,
    comments and likes.
    """
    feed_activity = School_Post.objects.all()
    return render(request, 'school_app/feed.html', {'feed_activity': feed_activity})
    