from django.db import models
from django.contrib.auth.models import User

class VocabList(models.Model):
	author = models.ForeignKey(User,on_delete=models.CASCADE)
	title = models.CharField(max_length=30)
	post_date = models.DateTimeField()
	#Allow people to restrict their list?
	#private = models.BooleanField(default=False)

class VocabWord(models.Model):
	vocabList = models.ForeignKey(VocabList, on_delete=models.CASCADE)
	word = models.CharField(max_length=50)
	definition = models.CharField(max_length=250)
	audioClip = models.FileField(null=True, blank=True, upload_to='vocab/audio/')

class CheckOff(models.Model):
	vocabWord = models.ForeignKey(VocabWord, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField()