from django.contrib import admin
from .models import Quiz, Question, RadioOption, Submission, Answer
# Register your models here.
class QuestionInline(admin.StackedInline):
	model = Question
class QuizAdmin(admin.ModelAdmin):
	inlines = [QuestionInline]

class AnswerInline(admin.StackedInline):
	model = Answer
class SubmissionAdmin(admin.ModelAdmin):
	inlines = [AnswerInline]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
admin.site.register(RadioOption)
admin.site.register(Submission, SubmissionAdmin)