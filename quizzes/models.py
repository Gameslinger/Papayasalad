from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Quiz(models.Model):
	title = models.CharField(max_length=50)
	author = models.ForeignKey(User,models.CASCADE, null=True)
	publishDate = models.DateTimeField()
	#Link to publish user
	#Post date?
	def __str__(self):
		return self.title
		
	def delete(self):
		for question in self.question_set.all():
			for answer in question.answer_set.all():
				answer.delete()
			if question.response_type == "RB":
				for option in question.radiooption_set.all():
					option.delete()
				question.delete()
				for submission in self.submission_set.all():
					submission.delete()
		super().delete()
class Question(models.Model):
	RESPONSE_TYPES = [
		('TF', 'Text Field'),
		('RB', 'Radio Button'),#TODO: add support for check boxes?
	]
	order = models.IntegerField(default=-1)
	text = models.CharField(max_length=300)
	quiz = models.ForeignKey(Quiz,models.CASCADE)
	correctAnswer = models.CharField(max_length=100, blank=True)
	response_type = models.CharField(max_length=2, choices=RESPONSE_TYPES, default='TF') #Make this cleaner https://docs.djangoproject.com/en/3.0/ref/models/fields/#field-options
	point_value = models.IntegerField(default=0)
	
	def __str__(self):
		return "\"{question}\" (Answer: \"{answer}\", {value} points)".format(value=self.point_value,question=self.text,answer=self.correctAnswer)

class RadioOption(models.Model):
	label = models.CharField(max_length=30)
	question = models.ForeignKey(Question,models.CASCADE)
	def __str__(self):
		return "Option: "+self.label

class Submission(models.Model):
	quiz = models.ForeignKey(Quiz,models.CASCADE)
	user = models.ForeignKey(User,models.CASCADE)
	timestamp = models.DateTimeField()
	score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	def __str__(self):
		return "{quiz}: {username} scored {score}% on {date}".format(quiz=str(self.quiz),score=self.score,username=self.user.username, date=self.timestamp.strftime("%b/%d/%Y at %I:%M %p"))
class Answer(models.Model):
	text = models.CharField(max_length=100, blank=True)
	submission = models.ForeignKey(Submission, models.CASCADE)
	question = models.ForeignKey(Question,models.CASCADE)
	def __str__(self):
		return "Answer: "+self.text
#def QuestionPhotos(models.Model):
#	question = models.ImageField()#TODO?