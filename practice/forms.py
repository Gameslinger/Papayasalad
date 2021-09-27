from django import forms
choices = (
	("QZ","Quiz"),
	("FL","File"),
	("UR","URL"),
	)

class LessonEditForm(forms.Form):
	resourceFileUpload = forms.FileField(required=False)
	urlTextField = forms.CharField(required=False, max_length=100, label="URL: ")
	newResourceType = forms.ChoiceField(choices=choices, required=False, label="Add: ")
	newResourceTitle = forms.CharField(required=False, max_length=30, label="Title: ")
	lessonRename = forms.CharField(required=False, max_length=50, label="Lesson rename: ")
	def __init__(self, resources, *args, **kwargs):
		super().__init__(*args,**kwargs)
		for r in resources:
			field_name = "delete_%s" %(r.id,)
			self.fields[field_name] = forms.BooleanField(required=False, label=r.title)
		
	def clean(self):
		delete_fields = set()
		#add_fields = set()
		for field_name in self.fields:
			if(field_name.startswith("delete_") and self.cleaned_data[field_name]):
				#TODO: Potential risk?!??!
				delete_fields.add(int(field_name[7:]))
			#elif(field_name.startswith("add_")):
				#add_fields.add(int(field_name[4:]))
		#self.cleaned_data["adding_resources"] = add_fields
		self.cleaned_data["delete_resources"] = delete_fields
		
	def get_resource_fields(self):
		for field_name in self.fields:
			if field_name.startswith("delete_"):
				yield self[field_name]