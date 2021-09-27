from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

RESOURCE_TYPES = (
	("QZ","Quiz"),
	("FL","File"),
	("UR","URL"),
	)

class Room(models.Model):
	title = models.CharField(blank=True,max_length=20)
	code = models.CharField(max_length=10,unique=True)
	post_date = models.DateTimeField('creation date')
	def __str__(self):
		return self.title

class Lesson(models.Model):
	title = models.CharField(max_length=50)
	post_date = models.DateTimeField('date posted')
	room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name="lessons")
	def __str__(self):
		return self.title

class Resource(models.Model):#Shift to generic contenttype to represent quiz, file, and url objects?
	title = models.CharField(max_length=30)
	link = models.CharField(max_length=100) #TODO:is this bad? Link to lesson resources
	lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name="resources")
	type = models.CharField(max_length=2,choices =RESOURCE_TYPES, default="UR")
	def __str__(self):
		return self.title

class Profile(models.Model):
	#line id?
	is_teacher = models.BooleanField(default=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	room = models.ForeignKey(Room, null=True, blank=True,on_delete=models.CASCADE)
	def __str__(self):
		return "%s's profile" % self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		p = Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()