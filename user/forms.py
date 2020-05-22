import unicodedata

from django import forms
from .models import Hobby, Profile, Gallery, BioDataModel, UserMoreInfoModel
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _



class SignUpForm(UserCreationForm, forms.ModelForm):
   
    first_name = forms.CharField(
    widget=forms.TextInput(attrs={
    'class':"form-control form-control-user",
    'id':"exampleFirstName",
    'placeholder':"First Name",
    })
    )

    last_name = forms.CharField(
    widget=forms.TextInput(attrs={
    'class':"form-control form-control-user",
    'id':"exampleLastName",
    'placeholder':"Last Name",
    })
    )
    
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
        'class':"form-control form-control-user",
        'id':"exampleEmail",
        'placeholder':"Email Address",
        })
        )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
        'class':"form-control form-control-user",
        'id':"exampleUsername",
        'placeholder':"Username",
        })
        )

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class':"form-control form-control-user",
            'id':"exampleInputPassword",
            'placeholder':"Password"
            }),

        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'class':"form-control form-control-user",
            'id':"exampleRepeatPassword",
            'placeholder':"Repeat Password"
            }),

        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )


    class Meta:
        model = User
        fields = ['first_name','last_name','email',
         'username', 'password1', 'password2'
        ]


class GalleryForm(forms.ModelForm):

    class Meta:
        model = Gallery
        fields = ['gallery_image']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']





class BioDataForm(forms.ModelForm):
    height = forms.TypedChoiceField(
        choices=BioDataModel.HEIGHT,
        widget=forms.Select(attrs={'class': 'selectpicker'}),
        coerce = str
        )
    
    eye_color = forms.TypedChoiceField(choices=BioDataModel.HAIR_COLOR,
     widget=forms.Select(attrs={'class': 'selectpicker'})
     )
    
    hair_color = forms.TypedChoiceField(choices=BioDataModel.HAIR_COLOR,
     widget=forms.Select(attrs={'class': 'selectpicker'})
     )
    complexion = forms.TypedChoiceField(choices=BioDataModel.COMPLEXION, 
        widget=forms.Select(attrs={'class': 'selectpicker'})
        )

    date_of_birth = forms.DateField()#input_formats=['%d-%m-%Y'])
    
    sex = forms.ChoiceField(choices=BioDataModel.SEX, label=('Gender'),
        widget=forms.Select(attrs={'class': 'selectpicker'})
        )

    religion = forms.ChoiceField(choices=BioDataModel.RELIGION_CH, 
    widget=forms.Select(attrs={'class': 'selectpicker'})
    )

    describe = forms.CharField(label=_("Short Desciption"),
        widget=forms.TextInput(attrs={
            'class':"form-control form-control-user",
            'id':"Desciption",
            'placeholder':"Tell something about you.",
            "rows": 20,
            "cols": 120,
            }),
    )

    institution = forms.CharField(label=_("Enter your Institution name"),
        widget=forms.TextInput(attrs={
            'class':"form-control form-control-user",
            'id':"institute",
            'placeholder':"e.g Funaab",
            "rows": 10,
            "cols": 50,
            }),
    )


    class Meta:
        model = BioDataModel
        exclude = ('user','age',)


class UserMoreInfoForm(forms.ModelForm):
    hobby                     = forms.TypedMultipleChoiceField(
        choices=UserMoreInfoModel.HOBBIES, 
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker'}),
        coerce=str,
        help_text=_("You can select more than one options."),
        )
    do_you_take_alcohol = forms.TypedChoiceField(choices=UserMoreInfoModel.CH3, widget=forms.Select(attrs={'class': 'selectpicker'}), coerce = str)
    do_you_smoke = forms.TypedChoiceField(choices=UserMoreInfoModel.CH2, widget=forms.Select(attrs={'class': 'selectpicker'}), coerce = str)
    sport = forms.MultipleChoiceField(
        choices=UserMoreInfoModel.SPORT, 
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker'}),
        help_text=_("You can select more than one options."),
        )
    music = forms.MultipleChoiceField(
        choices=UserMoreInfoModel.MUSIC,
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker'}),
        help_text=_("You can select more than one options."),
        )

    class Meta:
        model = UserMoreInfoModel
        exclude = ('user',)