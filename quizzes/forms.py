from django import forms

RESPONSE_TYPES = [
		('TF', 'Text Field'),
		('RB', 'Radio Button'),#TODO: add support for check boxes?
	]

class QuizForm(forms.Form):
	def __init__(self, quiz, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#quiz = get_object_or_404(Quiz, pk=quiz_id)
		questions = quiz.question_set.order_by('order')
		for (i,q) in enumerate(questions):
			field_name = "question_%s" % (i,)
			if q.response_type == "TF":
				self.fields[field_name] = forms.CharField(label=q.text, max_length=100, required=False)
			elif q.response_type == "RB":
				responses = q.radiooption_set.all()
				choices = [(resp.label,resp.label) for resp in responses]
				self.fields[field_name] = forms.ChoiceField(label=q.text,choices=choices, widget=forms.RadioSelect, required=False)
			else:
				pass
	def clean(self):
		questions = {}
		i = 0
		field_name = 'question_%s' % (i,)
		while self.cleaned_data.get(field_name):
			question = self.cleaned_data[field_name]
			print(field_name)
			print(question)
			if question in questions:
				self.add_error(field_name, "Duplicate")
			else:
				questions[i] = question
			i+=1
			field_name = "question_%s" % (i,)
		self.cleaned_data["questions"] = questions

	
	def save(self):
		pass

	def get_question_fields(self):
		for field_name in self.fields:
			if field_name.startswith("question_"):
				yield self[field_name]

class EditQuizForm(forms.Form): #TODO: Implement to allow editting of quizzes
	ANSWER_CHOICES = (
		("1","Answer 1"),
		("2","Answer 2"),
		("3","Answer 3"),
		("4", "Answer 4"),
	)
	question_text = forms.CharField(max_length=300,required=False, label="Question: ")
	question_type = forms.ChoiceField(choices=RESPONSE_TYPES,required=False, label="Question Type: ")
	quiz_rename_field = forms.CharField(max_length=50,required=False, label="Rename quiz: ")
	point_value = forms.IntegerField(initial=1, label="Point value: ")
	answer_field_1 = forms.CharField(max_length=100, label="Answer: ", required=False)
	answer_field_2 = forms.CharField(max_length=100, label="Answer 2: ",required=False)
	answer_field_3 = forms.CharField(max_length=100, label="Answer 3: ",required=False)
	answer_field_4 = forms.CharField(max_length=100, label="Answer 4: ",required=False)
	correct_answer = forms.ChoiceField(choices=ANSWER_CHOICES, initial="Answer 1")
	def __init__(self, questions, *args, **kwargs):
		super().__init__(*args,**kwargs)
		for q in questions:
			field_name = "delete_%s" %(q.id,)
			self.fields[field_name] = forms.BooleanField(required=False, label=q.text)
			
	def clean(self):
		delete_fields = set()
		for field_name in self.fields:
			if(field_name.startswith("delete_") and self.cleaned_data[field_name]):
				delete_fields.add(int(field_name[7:]))
		self.cleaned_data["delete_questions"] = delete_fields
			
	def get_question_fields(self):
		for field_name in self.fields:
			if field_name.startswith("delete_"):
				yield self[field_name]