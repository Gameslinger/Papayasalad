from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from .forms import LessonEditForm
from .models import Lesson, Resource
from quizzes.models import Quiz
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone

import urllib.parse #Remove this dependency when uploading files that have to be url encoded isnt a problem
import os #TODO: Should file creation/deletion be moved?


@login_required
def index(request):
	if(request.user.profile.room is not None):
		room = request.user.profile.room
		if(request.method=="POST" and request.user.profile.is_teacher and request.POST.get("addLesson")):
			lesson = Lesson(title="New Lesson", post_date=timezone.now(), room=room)
			lesson.save()
		latest_lesson_list = room.lessons.order_by('-post_date')
		template = loader.get_template('practice/index.html')
		context = {
			'is_teacher': request.user.profile.is_teacher,
			'latest_lesson_list': latest_lesson_list,
			'room_name': room.title,
		}
		return HttpResponse(template.render(context, request))
	return HttpResponse("Looks like you aren't part of any classes")#TODO: link to join class option
@login_required
def edit(request, lesson_id):
	#If the user isn't a teacher, they can't edit the lesson
	if(not request.user.profile.is_teacher): raise PermisionDenied #TODO: Switch from profile attribute to user group?
	lesson = get_object_or_404(Lesson,pk=lesson_id)
	lessonResources = lesson.resources.all()
	if(request.method == "POST"):
		form = LessonEditForm(lessonResources,request.POST)
		if form.is_valid():
			if request.POST.get("rename"):
				newLessonName = form.cleaned_data["lessonRename"]
				if(newLessonName):
					lesson.title= newLessonName
					lesson.save()
			elif request.POST.get("delete_lesson"):#TODO remove redundancy and clean up deletion
				for resource in lessonResources:
					if(resource.type=="QZ"):
						#Delete quiz. TODO: cleaner way to do this?
						id = int(resource.link[9:-1])#/quizzes/<id>/
						try:
							quiz.delete()
						except:#TODO: correct handling if quiz gets deleted on different page than lesson edit
							pass
					elif(resource.type=="FL"):
						os.remove(os.path.join(settings.MEDIA_ROOT,resource.link[7:]))#TODO: This could be dangerous!
					resource.delete()
				lesson.delete()
				return redirect("/practice")
			elif request.POST.get("delete"): #TODO: override delete function for resources to delete associated resources by themselves
				removing = form.cleaned_data["delete_resources"]
				for field in removing:
					resource = Resource.objects.get(pk=field)
					if(resource.type=="QZ"):
						#Delete quiz. TODO: cleaner way to do this?
						id = int(resource.link[9:-1])#/quizzes/<id>/
						try:
							quiz.delete()
						except:#TODO: correct handling if quiz gets deleted on different page than lesson edit
							pass
					elif(resource.type=="FL"):
						os.remove(os.path.join(settings.MEDIA_ROOT,resource.link[7:]))#TODO: This could be dangerous!
					resource.delete()
			#If user is adding:
			elif request.POST.get("add"):
				addType = form.cleaned_data["newResourceType"]
				#Add quiz:
				if(addType=="QZ"):
					quizTitle = form.cleaned_data["newResourceTitle"]
					if(quizTitle):
						quiz = Quiz(title=quizTitle, author = request.user, publishDate=timezone.now())
						quiz.save()
						link = "/quizzes/%s/" % (quiz.id,)
						resource = Resource(title=form.cleaned_data["newResourceTitle"],link=link,lesson=lesson, type="QZ")
						resource.save()
				elif(addType=="FL" and request.FILES.get("resourceFileUpload")):#TODO handle upload
					urlName = title=form.cleaned_data["newResourceTitle"]
					if urlName:
						resourceFile = request.FILES["resourceFileUpload"]
						lesson_resource_path = "lesson/%s/%s" % (lesson.id,resourceFile.name)
						fs = FileSystemStorage()
						filename = fs.save(lesson_resource_path, resourceFile)
						link = fs.url(lesson_resource_path)
						resource = Resource(title=urlName,link=link,lesson=lesson, type="FL")
						resource.save()
				elif(addType=="UR"):
					urlName = form.cleaned_data["newResourceTitle"]
					urlLink = form.cleaned_data["urlTextField"]
					if urlName and urlLink:
						resource = Resource(title=urlName, link=urlLink,lesson=lesson,type="UR")
						resource.save()
					
	lessonResources = lesson.resources.all()
	form = LessonEditForm(lessonResources) 
	context = { #TODO: Clean up way to access quiz id? instead of url link?
		"quiz_resource_list": [resource for resource in lessonResources if resource.type == "QZ"],
		"lesson_name":lesson.title,
		"form":form,
		}
	return render(request, template_name="practice/edit.html",context=context)

	