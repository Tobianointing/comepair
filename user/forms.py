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



# class UserMoreInfoForm(forms.Form):
#     HOBBIES = [
#     ('Reading', 'Reading'), ('Watching TV', 'Watching TV'), ('Family Time', 'Family Time'), 
#     ('Going to Movies', 'Going to Movies'), ('Fishing', 'Fishing'), ('Computer', 'Computer'), 
#     ('Gardening', 'Gardening'), ('Walking', 'Walking'), ('Exercise', 'Exercise'), 
#     ('Listening to Music', 'Listening to Music'), ('Entertaining', 'Entertaining'), 
#     ('Hunting', 'Hunting'), ('Team Sports', 'Team Sports'), ('Shopping', 'Shopping'), 
#     ('Traveling', 'Traveling'), ('Sleeping', 'Sleeping'), ('Socializing', 'Socializing'), 
#     ('Sewing', 'Sewing'), ('Church Activities', 'Church Activities'), ('Relaxing', 'Relaxing'), 
#     ('Playing Music', 'Playing Music'), ('Housework', 'Housework'), ('Crafts', 'Crafts'), 
#     ('Watching Sports', 'Watching Sports'), ('Bicycling', 'Bicycling'), ('Playing Cards', 'Playing Cards'), 
#     ('Cooking', 'Cooking'), ('Swimming', 'Swimming'), ('Camping', 'Camping'), ('Writing', 'Writing'), 
#     ('Animal Care', 'Animal Care'), ('Painting', 'Painting'), ('Running', 'Running'), ('Dancing', 'Dancing'), 
#     ('Tennis', 'Tennis'), ('Theater', 'Theater'), ('Beach', 'Beach'), 
#     ('Volunteer Work', 'Volunteer Work')
#     ]

#     CHOICES_YESorNO = [
#     (0, 'Yes'),
#     (1, 'No')
#     ]

#     CH2 = [
#     ('once a year', 'once a year'), 
#     ('once a month', 'once a month'), 
#     ('once a week', 'once a week'), 
#     ('daily', 'daily')
#     ]

#     MUSIC = [
#         ('rap', 'rap'), ('gospel', 'gospel'),
#         ('jazz', 'jazz'), ('blues/soul', 'blues/soul'),
#         ('hip-hop', 'hip-hop'), ('oldies', 'oldies'),
#         ('classical', 'classical'), ('R&B', 'R&B'),
#         ('reggae', 'reggae'), ('others', 'others')
#         ]

#     SPORT = [
#         ('volleyball', 'volleyball'), ('badminton', 'badminton'), 
#         ('running', 'running'), ('basketball', 'basketball'), 
#         ('gymnastics', 'gymnastics'), ('table tennis', 'table tennis'),
#         ('handball', 'handball'), ('football', 'football'),
#         ('martial arts', 'martial arts'), ('squash', 'squash'), 
#         ('other', 'other')
#         ]

#     hobby                     = forms.TypedMultipleChoiceField(choices=HOBBIES, widget=forms.SelectMultiple(attrs={'class': 'selectpicker'}), coerce=str)
#     do_you_take_alcohol       = forms.TypedChoiceField(choices=CH2, widget=forms.Select(attrs={'class': 'selectpicker'}), coerce = str)
#     do_you_smoke              = forms.TypedChoiceField(choices=CH2, widget=forms.Select(attrs={'class': 'selectpicker'}), coerce = str)
#     sport                     = forms.MultipleChoiceField(choices=SPORT, widget=forms.SelectMultiple(attrs={'class': 'selectpicker'}))
#     music                     = forms.MultipleChoiceField(choices=MUSIC, widget=forms.SelectMultiple(attrs={'class': 'selectpicker'}))


# class BioDataForm(forms.Form):
#     HEIGHT = [
#     ('< 60inches(152.40cm)', '< 60inches(152.40cm)'),
#     ('> 60inches(152.40cm) but < 65inches(165.10cm)', '> 60inches(152.40cm) but < 65inches(165.10cm)'),
#     ('> 65inches(165.10cm) but < 70inches(177.80cm)', '> 65inches(165.10cm) but < 70inches(177.80cm)'), 
#     ('> 70inches(177.80) but < 75inches(190.50cm)', '> 70inches(177.80) but < 75inches(190.50cm)'),
#     ('> 75inches(190.50cm) but < 80inches(203.20cm)', '> 75inches(190.50cm) but < 80inches(203.20cm)'),
#     ('> 80inches(203.20cm) but < 85inches(215.90cm)', '> 80inches(203.20cm) but < 85inches(215.90cm)'),
#     ('> 85inches(215.90cm) but < 90inches(228.6)', '> 85inches(215.90cm) but < 90inches(228.6)'),
#     ('> 60inches(152.40cm)', '> 60inches(152.40cm)')
#     ]


#     COMPLEXION = [
#         ('very light', 'very light'),
#         ('light', 'light'),
#         ('brown/chocolate',
#         'brown/chocolate'),
#         ('dark brown', 'dark brown'),
#         ('very dark', 'very dark')
#         ]


#     HAIR_COLOR = [
#     ('light', 'light'),
#     ('brown', 'brown'),
#     ('black', 'black')
#     ]

#     RELIGION_CH = [
#     ('christainity', 'christainity'),
#     ('islam', 'islam'),
#     ('traditional', 'traditional'),
#     ('atheist', 'atheist')
#     ]

#     SEX = [
#     ('male', 'male'),
#     ('female', 'female')
#     ]

#     height = forms.TypedChoiceField(
#         choices=HEIGHT,
#         widget=forms.Select(attrs={'class': 'selectpicker'}),
#         coerce = str
#         )
    
#     eye_color = forms.TypedChoiceField(choices=HAIR_COLOR,
#      widget=forms.Select(attrs={'class': 'selectpicker'})
#      )
    
#     hair_color = forms.TypedChoiceField(choices=HAIR_COLOR,
#      widget=forms.Select(attrs={'class': 'selectpicker'})
#      )
#     complexion = forms.TypedChoiceField(choices=COMPLEXION, 
#         widget=forms.Select(attrs={'class': 'selectpicker'})
#         )

#     date_of_birth = forms.DateField(input_formats=['%d/%m/%Y'])
    
#     sex = forms.ChoiceField(choices=SEX, label=('Gender'),
#         widget=forms.Select(attrs={'class': 'selectpicker'})
#         )

#     religion = forms.ChoiceField(choices=RELIGION_CH)

#     describe = forms.CharField(label=_("Short Desciption"),
#         widget=forms.TextInput(attrs={
#             'class':"form-control form-control-user",
#             'id':"Desciption",
#             'placeholder':"Tell something about you.",
#             "rows": 20,
#             "cols": 120,
#             }),
#     )


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

    religion = forms.ChoiceField(choices=BioDataModel.RELIGION_CH)

    describe = forms.CharField(label=_("Short Desciption"),
        widget=forms.TextInput(attrs={
            'class':"form-control form-control-user",
            'id':"Desciption",
            'placeholder':"Tell something about you.",
            "rows": 20,
            "cols": 120,
            }),
    )

    class Meta:
        model = BioDataModel
        exclude = ('user','age',)


class UserMoreInfoForm(forms.ModelForm):
    hobby                     = forms.TypedMultipleChoiceField(choices=UserMoreInfoModel.HOBBIES, widget=forms.SelectMultiple(attrs={'class': 'selectpicker'}), coerce=str)
    do_you_take_alcohol       = forms.TypedChoiceField(choices=UserMoreInfoModel.CH2, widget=forms.Select(attrs={'class': 'selectpicker'}), coerce = str)
    do_you_smoke              = forms.TypedChoiceField(choices=UserMoreInfoModel.CH2, widget=forms.Select(attrs={'class': 'selectpicker'}), coerce = str)
    sport                     = forms.MultipleChoiceField(choices=UserMoreInfoModel.SPORT, widget=forms.SelectMultiple(attrs={'class': 'selectpicker'}))
    music                     = forms.MultipleChoiceField(choices=UserMoreInfoModel.MUSIC, widget=forms.SelectMultiple(attrs={'class': 'selectpicker'}))

    class Meta:
        model = UserMoreInfoModel
        exclude = ('user',)