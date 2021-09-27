from django import forms
from django.contrib.auth.forms import UserCreationForm
from practice.models import Room
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
	roomCode = forms.CharField(max_length=10,required=True)
	
	def clean_roomCode(self):
		roomCode = self.cleaned_data["roomCode"]
		if(not Room.objects.filter(code=roomCode).exists()):
			raise ValidationError("Room code does not exist")
		return roomCode