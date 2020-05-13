from django.db import models
from django.contrib.auth.models import User
import ast

# Create your models here.
class ListField(models.TextField):
	description = "Stores a python list"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def from_db_value(self, value, expression, connection):
		if value is None:
			return value
		if isinstance(value, str):
			return value.split(',')

	def to_python(self, value):
		if not value:
			value = []
		if isinstance(value, list):
			return value
		if isinstance(value, str):
			return ast.literal_eval(value)

	def get_prep_value(self, value):
		if value is None:
			return value
		if value is not None and isinstance(value, str):
			return value
		if isinstance(value, list):
			return ','.join(value)

	def value_to_string(self, obj):
		value = self.value_from_object(obj)
		return self.get_prep_value(value)


class Answer(models.Model):
	questionId = models.IntegerField()
	answer = models.IntegerField()
	acceptableAnswers = ListField()
	importance = models.IntegerField()

	def __str__(self):
		return f'Answer {str(self.questionId)}'


class User_Answer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=1)
	answered = models.ManyToManyField(Answer)

	def __str__(self):
		return self.user.username

class Question(models.Model):
	question_text = models.CharField(max_length=200)

	def __str__(self):
		return f'{self.question_text[:20]} ...?'

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	acceptableAnswers = models.CharField(max_length=200, default='haa')

	def __str__(self):
		return self.choice_text

		
# quest generator func 
# def qc(s,l):
# 	q = Question.objects.create(question_text=s)
# 	for i in l:
# 		q.choice_set.create(choice_text=i)
# 	return 0