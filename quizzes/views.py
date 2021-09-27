from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from .models import *
from .forms import QuizForm, EditQuizForm
from django.utils import timezone

import json

@login_required
def index(request):
	#quizzes = Quiz.objects.all()
	context = {
		#"quiz_list": quizzes,
	}
	return render(request, template_name="quizzes/index.html", context=context)

@login_required
def fill(request,quiz_id):
	"""
	View for filling out a quiz
	"""
	quiz = get_object_or_404(Quiz, pk=quiz_id)
	if request.method == 'POST':
		form = QuizForm(quiz,request.POST)
		if form.is_valid():
			percent = calculate_quiz_score(user=request.user,quiz=quiz,answer_list=form.cleaned_data['questions'])
			context = {
			"quiz":quiz,
			"score": percent,
			}
			return render(request, template_name="quizzes/complete.html", context=context)
	else:
		quizForm = QuizForm(quiz=quiz)
		context = {
			'quiz_name':quiz.title,
			'form':quizForm,
			"isAuthenticated":request.user.is_authenticated,
			"isTeacher":request.user.profile.is_teacher,
		}
		return render(request, template_name='quizzes/fill.html',context=context)
	
def calculate_quiz_score(user, quiz, answer_list):
	"""Helper function to calculate the score
		and store responses
	Args:
		user: user submitting quiz
		quiz: quiz model scoring against
		answer_list: cleaned list of answers 
			sorted ordinally based on the question
			it answers from fill submissions
			
	Returns:
		float of percentage of correct questions
			(with weighted point value)
	"""
	submission = Submission(quiz=quiz, user=user,timestamp=timezone.now())
	submission.save()#TODO: do I need to save it twice?
	questions = quiz.question_set.all()
	score = 0
	total = 0
	for q in questions:
		answer = answer_list.get(q.order)#TODO standardize starting to 1 or zero?
		print(answer)
		if answer == None: answer = ""
		#Correct answer:
		if(not q.correctAnswer or answer == q.correctAnswer):
			score+=q.point_value
		answerModel = Answer(text=answer,submission=submission, question=q)
		answerModel.save()
		total+=q.point_value
	if total != 0:
		percent = score/total*100
	else:
		percent = 100
	submission.score = percent
	submission.save()
	return percent
	
@login_required
def edit_quiz(request, quiz_id):
	if(not request.user.profile.is_teacher): raise PermisionDenied #TODO: Switch from profile attribute to user group?
	quiz = get_object_or_404(Quiz, pk=quiz_id)
	questions = quiz.question_set.all()
	if(request.method == "POST"):
		form = EditQuizForm(questions, request.POST)
		if form.is_valid():
			if request.POST.get("rename_quiz"):#If rename field isn't empty:
				quizTitle = form.cleaned_data["quiz_rename_field"]
				if(quizTitle):
					quiz.title=quizTitle
					quiz.save()
			elif request.POST.get("delete_quiz"):
				quiz.delete()
				return redirect("/quizzes/")
			elif request.POST.get("delete"):#If deleting selected fields...
				for question_id in form.cleaned_data["delete_questions"]:
					question = Question.objects.get(pk=question_id)
					for answer in question.answer_set.all(): #Remove all responses for that question...
						answer.delete()
					if question.response_type == "RB":
						for option in question.radiooption_set.all():
							option.delete()
					question.delete()#Cascade the order numbers when a question is deleted
			elif request.POST.get("add"): 
				if form.cleaned_data["question_type"] == "TF":
					question = Question(order=len(questions),text=form.cleaned_data["question_text"],quiz=quiz,correctAnswer=form.cleaned_data["answer_field_1"], response_type=form.cleaned_data["question_type"], point_value=form.cleaned_data["point_value"])
					question.save()
				elif form.cleaned_data["question_type"] == "RB":
					correctAnswerNum = form.cleaned_data["correct_answer"]
					correctAnswer = form.cleaned_data["answer_field_%s" % (correctAnswerNum)]
					question = Question(order=len(questions),text=form.cleaned_data["question_text"],quiz=quiz,correctAnswer=correctAnswer, response_type=form.cleaned_data["question_type"], point_value=form.cleaned_data["point_value"])
					question.save()
					for i in range(4):#Really dirty trick to add 4 answers to radio button... fix me!
						field_name = form.cleaned_data["answer_field_%s" % (i+1,)]
						if(field_name):#Field has a value
							option = RadioOption(label=form.cleaned_data["answer_field_%s" % (i+1,)],question=question)
							option.save()
	questions = quiz.question_set.all()
	form = EditQuizForm(questions=questions)
	context = {
		"form":form,
		"quiz":quiz,
		"isAuthenticated":request.user.is_authenticated,
	}
	return render(request, template_name="quizzes/edit.html", context=context)
@login_required
def score_quiz(request, quiz_id):
	if(not request.user.profile.is_teacher): raise PermissionDenied #TODO: Switch from profile attribute to user group?
	quiz = get_object_or_404(Quiz, pk=quiz_id)
	submissions = quiz.submission_set.order_by("-timestamp").all()
	context = {
		"quiz": quiz,
		"submissions":submissions,
		"isAuthenticated":request.user.is_authenticated,
	}
	return render(request, template_name="quizzes/score.html", context=context)
	
#Good query rest api? Or should it just be part of the other quiz list page?
@login_required
def search_quizzes(request):
	search = request.GET.get("search","")
	quiz_names = list(Quiz.objects.filter(title__icontains=search).order_by("-publishDate").values('title','id', 'author','publishDate'))
	for row in quiz_names:
		if row.get('author'):
			row['author'] = User.objects.get(pk=row['author']).username
		else:
			row['author'] = "<Unknown>"
		row['publishDate'] = row['publishDate'].strftime("%b/%d/%Y at %I:%M %p")
	return HttpResponse(json.dumps(quiz_names))#TODO specify pages for lots of quizzes?