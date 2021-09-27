from django import forms

class VocabListEditForm(forms.Form):
	newTitle = forms.CharField(required=False, max_length=30, label="Edit Title: ")
	newWord = forms.CharField(required=False, max_length=50, label="Word: ")
	definition = forms.CharField(required=False, max_length=250, label="Definition: ")
	#TODO: Restrict file to audio codec? Ex: wav
	audioClip = forms.FileField(required=False)
	#checkOffWords(toggle?), deleteWords
	
	def __init__(self, words, *args, **kwargs):
		super().__init__(*args,**kwargs)
		for word in words:
			delete_field_name = "delete_%s" % (word.id,)
			toggle_field_name = "check_%s" % (word.id,)
			self.fields[delete_field_name] = forms.BooleanField(required=False)
			self.fields[toggle_field_name] = forms.BooleanField(required=False,  label=word.word+": "+word.definition)

	#TODO: Update to use fields in word_fields_list instead of brute force string comparison?
	def clean(self):
		delete_words = set()
		toggle_words = set()
		for field_name in self.fields:
			if self.cleaned_data.get(field_name):
				if(field_name.startswith("delete_")):
					#TODO: Potential risk?!??!
					delete_words.add(int(field_name[7:]))
				elif(field_name.startswith("check_")):
					toggle_words.add(int(field_name[6:]))
		self.cleaned_data["delete_words"] = delete_words
		self.cleaned_data["toggle_words"] = toggle_words

	def get_word_fields(self):
		for field_name in self.fields:
			if field_name.startswith("delete_") or field_name.startswith("check_"):
				yield self[field_name]