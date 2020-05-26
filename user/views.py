from django.shortcuts import render, redirect, get_object_or_404
import os
from django.conf import settings
from django.templatetags.static import static
from django.contrib.auth.models import User
from match.views import notification

from .forms import ( 
	SignUpForm, 
	UserMoreInfoForm, 
	BioDataForm,
	GalleryForm,
	UserUpdateForm,
	ProfileUpdateForm,
	GalleryNewForm
	)
from .models import (
	UserMoreInfoModel, 
	Profile,  
	OthersProfiles, 
	BioDataModel,
	GalleryNew
	)
from django.contrib.auth.decorators import login_required 
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.urls import reverse


# Create your views here.

#SIGNUP VIEW
def signup(request):
	if  request.method =='POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			return redirect('quiz_intro')
	else:
		form = SignUpForm()
	context = {
		'form': form,
	}
	return render(request, 'registration/signup.html', context)

#USER-INFO VIEW
def hobb(request):
	if request.method == 'POST':
		form = UserMoreInfoForm(request.POST)
		key_list = ['hobby', 'do_you_take_alcohol', 'do_you_smoke',
				 'do_you_get_angry_easily', 'your_ideal_partner_should']
		int_dict = {}
		if form.is_valid():
			print(form.cleaned_data)
			clean = form.cleaned_data

			newitem = UserMoreInfoModel()
			newitem.user = request.user
			newitem.hobby = clean['hobby']
			newitem.do_you_smoke = clean['do_you_smoke']
			newitem.do_you_take_alcohol = clean['do_you_take_alcohol']
			newitem.sport = clean['sport']
			newitem.music = clean['music']
			newitem.save()
		
			return redirect('post-home')
	else:
			form = UserMoreInfoForm()

	context = {
	'form': form
	}
	return render(request, 'user/hobbies.html', context)	

#BIODATA VIEW
@login_required
def biodata(request):
	if request.method == 'POST':
		form = BioDataForm(request.POST)
		if form.is_valid():
			newitem = BioDataModel()
			print(form.cleaned_data)
			newitem.user = request.user
			newitem.height = form.cleaned_data['height']
			newitem.eye_color = form.cleaned_data['eye_color']
			newitem.hair_color = form.cleaned_data['hair_color']
			newitem.complexion = form.cleaned_data['complexion']
			newitem.date_of_birth = form.cleaned_data['date_of_birth']
			newitem.describe = form.cleaned_data['describe']
			newitem.religion = form.cleaned_data['religion']
			newitem.sex = form.cleaned_data['sex']
			newitem.institution = form.cleaned_data['institution']
			newitem.save()

			return redirect('hobbies')
	else:
			form = BioDataForm()
	context = {
	'form': form
	}
	return render(request, 'user/biodata.html', context)	

#USER PROFILE VIEW
@login_required
def profile(request):
	user = User.objects.get(id=request.user.id)
	context = notification(request)
	context['user'] = user
	return render(request, 'user/profile.html', context)

# Images Gallery view Edited version 1.2
def gallery(request):
	user = User.objects.get(username=request.user.username)
	if  request.method =='POST':
		# # gallery_image = request.POST.get('galleryimage')
		# print(gallery_image)
		# print('.....hey.....')
		# user.gallerynew_set.create(gallery_image=gallery_image)
		form = GalleryNewForm(request.POST, request.FILES)
		if form.is_valid():
			print(form.cleaned_data)
			user.gallerynew_set.create(gallery_image=form.cleaned_data.get('image'))
			# form.save()
			print('yeah!!')
			return redirect('gallery')
	else:
		form = GalleryNewForm()

	galleries = GalleryNew.objects.filter(user=request.user)

	context = {
		"galleries": galleries,
		'user': user,
		'form': form
	}
	context.update(notification(request))
	return render(request, "user/gallery.html", context)

#USER INTEREST VIEW
@login_required
def interest(request):
	user = User.objects.get(id=request.user.id)
	context = {'user': user}
	context.update(notification(request))
	return render(request, 'user/interest.html', context)

#USER PROFILE, BIODATA & USERINFO UPADATE VIEW
@login_required
def profile_update(request):
	if  request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		b_form = BioDataForm(request.POST, instance=request.user.biodatamodel)
		h_form = UserMoreInfoForm(request.POST, instance=request.user.usermoreinfomodel)

		if u_form.is_valid() and p_form.is_valid() and b_form.is_valid() and h_form.is_valid():
			u_form.save()
			p_form.save()
			b_form.save()
			h_form.save()
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
		b_form = BioDataForm(instance=request.user.biodatamodel)
		h_form = UserMoreInfoForm(instance=request.user.usermoreinfomodel)

	context = {
	'u_form': u_form,
	'p_form': p_form,
	'b_form': b_form,
	'h_form': h_form
	}
	
	return render(request, 'user/update.html', context)

#OTHER USER PROFILE
@login_required
def other_profiles(request, slug):
	obj = User.objects.get(username=slug)
	context = { 
			'object': obj
	} 
	context.update(notification(request))
	return render(request, 'user/otherprofiles.html', context)

#OTHER USER GALLERY
@login_required		
def other_gallery(request, slug):
	user = User.objects.get(username=slug)
	obj =  GalleryNew.objects.filter(user=user)

	context = { 
			'galleries': obj,
			'object': user
	}
	context.update(notification(request))
	return render(request, "user/othergallery.html", context)

#OTHER USER INTEREST
def other_interest(request, slug):
	user = User.objects.get(username=slug)
	context = {'object': user}
	context.update(notification(request))
	return render(request, 'user/othersinterest.html', context)	


