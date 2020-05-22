from django.shortcuts import render, redirect, get_object_or_404
import os
from django.conf import settings
from django.templatetags.static import static
from django.contrib.auth.models import User
from .forms import ( 
	SignUpForm, 
	UserMoreInfoForm, 
	BioDataForm,
	GalleryForm,
	UserUpdateForm,
	ProfileUpdateForm,
	)
from .models import (
	UserMoreInfoModel, 
	Profile,  
	OthersProfiles, 
	BioDataModel
	)
from django.contrib.auth.decorators import login_required 
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.urls import reverse


# Create your views here.
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
		
			return redirect('home')
	else:
			form = UserMoreInfoForm()

	context = {
	'form': form
	}
	return render(request, 'user/hobbies.html', context)	

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


@login_required
def profile(request):
	user = User.objects.get(id=request.user.id)
	context = {'user': user}
	return render(request, 'user/profile.html', context)

# @login_required
# class ProfileDetailView(DetailView):
# 	model = OthersProfiles


# Images Gallery view
def gallery(request):
	if  request.method =='POST':
		form = GalleryForm(request.POST, request.FILES, instance=request.user.gallery)
		if form.is_valid():
			form.save()
			print('yeah!!')
			return redirect('gallery')
	else:
		form = GalleryForm()

	user = User.objects.get(id=request.user.id)
	MEDIA_URL = settings.MEDIA_URL
	path = settings.MEDIA_ROOT
	img_list = os.listdir(path + f'/user_{request.user.id}')
	print(MEDIA_URL)

	context = {
	'images' : img_list, 
	'MEDIA_URL': MEDIA_URL,
	'user': user,
	'form': form
	}
	return render(request, "user/gallery.html", context)


@login_required
def interest(request):
	user = User.objects.get(id=request.user.id)
	context = {'user': user}
	return render(request, 'user/interest.html', context)

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

@login_required
def other_profiles(request, slug):
	obj = User.objects.get(username=slug)
	context = { 
			'object': obj
	} 
	return render(request, 'user/otherprofiles.html', context)

@login_required		
def other_gallery(request, slug):
	user = User.objects.get(username=slug)
	MEDIA_URL = settings.MEDIA_URL
	path = settings.MEDIA_ROOT
	img_list = os.listdir(path + f'/user_{user.id}')
	print(MEDIA_URL)

	context = {
	'images' : img_list, 
	'MEDIA_URL': MEDIA_URL,
	'object': user,
	
	}
	return render(request, "user/othergallery.html", context)

def other_interest(request, slug):
	user = User.objects.get(username=slug)
	context = {'object': user}
	return render(request, 'user/othersinterest.html', context)	


# @login_required
# def secret_page(request):
# 	return render(request, 'secret_page.html')

# class SecretPage(LoginRequiredMixin, TemplateView):
# 	template_name = 'secret_page.html'