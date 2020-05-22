from django.templatetags.static import static

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from django.forms.models import model_to_dict
from django.urls import reverse
from .models import (
	Answer, 
	User_Answer,
	Question 
	)
from chat.models import Notification

from chat.models import Thread
from itertools import chain
import math
import sys
import json
from pqdict import PQDict

IMPORTANCE = [0, 1, 10, 50, 250]

# Create your views here.
@login_required
def quiz_intro(request):
	return render(request, 'match/quiz_intro.html')

def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
    	data[f.name] = [model_to_dict(i) for i in f.value_from_object(instance)]
    return data

def match_algorithm(profiles, user_answer):
	profiles_dict = {'profiles_':[]}

	output = {'results': []}
	matched_users = []

	for i in profiles:
		t = to_dict(i)
		for a in t['answered']:
			del a['id']
		profiles_dict['profiles_'].append(t)


	#Calculating (Algorithms starts) here
	profiles = profiles_dict['profiles_']
	# print(profiles)
	for profile in profiles:
		pq = PQDict()
		no_of_profiles = 0
		matches=[]
        
		# The output for this profile in JSON format 
		profile_output = {'profileId': profile['user'],
				'matches': []}

		for other_profile in profiles:
			if other_profile['user'] == profile['user']:
			# dont calculate against our own profile
				continue
			# Calculate match percentage with OKCupid's formula
			match_score = round((math.sqrt(satisfaction(profile, other_profile) * satisfaction(other_profile, profile))) * 100)

			# Add the first ten matches to a min-heap (PQDict) 
			if len(pq) < 11:
				pq.additem(other_profile['user'],match_score)
			else:
				if match_score > pq.popitem()[1]:
					pq.additem(other_profile['user'],match_score)
				else:
					continue
	
		for i in range(len(pq)):
			key,value = pq.popitem()
			temp = {'profileId': key,
				'score': value}
			matches.append(temp)

			# Reverse the heap and store it in the output for that profile
		profile_output['matches'] = matches[::-1]
		output['results'].append(profile_output)
	print('oout')
	print(output['results'])

	print(user_answer.user.id)
	for i in output['results']:
		if i['profileId'] == user_answer.user.id:
			w = i
	print(w)		
	for i in w['matches']:
		if i['score'] >= 0.3:
			matched_users.append([i['profileId'], i['score']])

	all_users = User.objects.all()
	logged_user = User.objects.get(id=user_answer.user.id)
	print(matched_users)

	context = {
	'all_users': all_users,
	'matched_users': matched_users
	}
	
	return context

def satisfaction(profile, other_profile):
	
	# Make a dictionary with questionId as key and answer as value
	my_answers = {answer['questionId']: answer for answer in profile['answered']}
	# print('myanswer----')
	# print(my_answers)
	otherp_answers = {answer['questionId']: answer for answer in other_profile['answered']}
    
	correct_points = 0
	possible_points = 0
	for answer in otherp_answers:
		if answer in my_answers:

			# Check if we both answered this question.
			answer_value = IMPORTANCE[my_answers[answer]['importance']]
			# print(answer_value)
			possible_points += answer_value
			
			# print(possible_points)
			# print('\n')
			# Other_profile gets correct points if their answer is in my acceptableAnswers
			if str(otherp_answers[answer]['answer']) in my_answers[answer]['acceptableAnswers']:
				correct_points += answer_value
		print(possible_points)
	if possible_points == 0:
		possible_points = 1
	return float(correct_points) / float(possible_points)

def notification(request):
        notification = Notification.objects.filter(notification_user=request.user, notification_read=False).order_by('-notification_chat__timestamp')[:1]
        notification_read = Notification.objects.filter(notification_user=request.user, notification_read=True)
        return {
            'notification':notification,
            'notification_read':notification_read
        }
	
@login_required
def home(request):
	context = notification(request)
	return render(request, 'match/home.html', context)


def match(request):
	profiles = User_Answer.objects.all()
	user_answer = User_Answer.objects.get(user_id=request.user.id)

	context = match_algorithm(profiles, user_answer)
	
	return render(request, 'match/match.html', context)

	
@login_required
def question_page(request, questionId):
	IMPORTANCE = [
    'irrelevant',
    'little important',
    'some what important',
    'very important'
    ]
	question = get_object_or_404(Question, pk=questionId)
	p = User_Answer.objects.get(user_id=request.user.id)
	if request.method == 'POST':
		p.answered.add(Answer.objects.create(
			questionId=questionId,
		 	answer=int(request.POST.get('choice')),
		  	acceptableAnswers=request.POST.getlist('acceptableAnswer'),
		  	importance=int(request.POST.get('importance'))
		  	)
		)
		print(questionId)
		while questionId < 25:
			try:
				return redirect('question_page', f'{questionId + 1}')
			except TypeError:
				return redirect('question_page', questionId) 

		return redirect('biodata')

	print(request.POST)
	context= {
	'question': question,
	'importances': IMPORTANCE

	}
	return render(request, 'match/question_page.html', context)


