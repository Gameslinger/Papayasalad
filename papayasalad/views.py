from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from practice.models import Room, Profile
from papayasalad.forms import CustomUserCreationForm

def index(request):
	context = {
		"user":request.user,
	}
	return render(request, template_name="papayasalad/index.html", context=context)

def signout(request):
	if(request.user.is_authenticated):
		logout(request)
	return redirect('/')
		

def signup(request):
	errors=""
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			#Check if user has entered a correct room:
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			room = Room.objects.filter(code=form.cleaned_data['roomCode'])[0]#TODO: change to get instead of filter?
			user = authenticate(username=username, password=raw_password)
			user.profile.room = room
			user.profile.save()
			login(request,user)
			return redirect('/')
		errors = form.errors
		#If they didn't list a correct room, reserve the form
	form = CustomUserCreationForm()
	context = {
	'form': form,
	'errors':errors,
	}
	return render(request, 'signup.html', context)