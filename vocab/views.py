from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.files import File
from django.http import HttpResponse
from .models import *
from .forms import VocabListEditForm

import json
@login_required
def index(request):
	
	context = {
	
	}
	return render(request,template_name="vocab/index.html",context=context)
#TODO: fix submit buttons to relieve strain of processing everything on form submission at once.

@login_required
def viewList(request, list_id):
	vocabList = get_object_or_404(VocabList,pk=list_id)
	words = vocabList.vocabword_set.all()
	if request.method == "POST":
		print(request.POST.keys())
		form = VocabListEditForm(words,request.POST)
		if form.is_valid():
		#if request.POST.get("changeTitle"):
			newTitle = form.cleaned_data["newTitle"]
			if(newTitle):
				vocabList.title = newTitle
		#elif request.POST.get("addWord"):
			print("Adding word")
			newWord = form.cleaned_data["newWord"]
			newDefinition = form.cleaned_data["definition"]
			if(newWord and newDefinition):
				audioFile = None
				if request.FILES.get("audioClip"):
					audioFile = File(request.FILES["audioClip"])
				word = VocabWord(vocabList=vocabList, word=newWord, definition=newDefinition, audioClip=audioFile)
				word.save()
		#elif request.POST.get("deleteWords"):
			for id in form.cleaned_data["delete_words"]:
				word = VocabWord.objects.get(pk=id)
				word.delete()
	words = vocabList.vocabword_set.all()
	form = VocabListEditForm(words=words)
	context = {
		"form": form,
		"title":vocabList.title,
		"words":words,
	}
	return render(request, template_name="vocab/listView.html", context=context)
@login_required
def seach_vocabLists(request):
	search = request.GET.get("search","")
	list_names = list(VocabList.objects.filter(title__icontains=search).order_by("-post_date").values('title','id', 'author','post_date'))
	for row in list_names:
		if row.get('author'):
			row['author'] = User.objects.get(pk=row['author']).username
		else:
			row['author'] = "<Unknown>"
		row['post_date'] = row['post_date'].strftime("%b/%d/%Y at %I:%M %p")
	return HttpResponse(json.dumps(list_names))#TODO specify pages for lots of quizzes?