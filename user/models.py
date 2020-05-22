from django.db import models
from django.contrib.auth.models import User
import ast
from django.urls import reverse
from django.utils.text import slugify
import datetime



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


class Hobby(models.Model):
	hobbies = models.IntegerField()

# class UserMoreInfoModel(models.Model):
# 	user 					  = models.OneToOneField(User, on_delete=models.CASCADE)
# 	hobby                     = ListField()
# 	do_you_take_alcohol       = models.CharField(max_length=200)
# 	do_you_smoke              = models.CharField(max_length=200)
# 	sport                     = ListField()
# 	music                     = ListField()

# 	def __str__(self):
# 		return f'{self.user.username} Hobbies'

# class BioDataModel(models.Model):
# 	user = models.OneToOneField(User, on_delete=models.CASCADE)
# 	height = models.CharField(max_length=200)
# 	eye_color = models.CharField(max_length=200)
# 	hair_color = models.CharField(max_length=200)
# 	complexion = models.CharField(max_length=200)
# 	date_of_birth = models.DateField(default='02/04/1999')
# 	age = models.IntegerField()
# 	describe = models.TextField(max_length=150, default='Short description')
# 	religion = models.CharField(max_length=50, default='christainity')
# 	sex = models.CharField(max_length=10, default='male')
     

# 	def save(self, *args, **kwargs):
# 		if self.date_of_birth.month > datetime.date.today().month:
# 			self.age = datetime.date.today().year - self.date_of_birth.year
# 		else:
# 			self.age = (datetime.date.today().year - self.date_of_birth.year) - 1 

# 		super(BioDataModel, self).save(*args, **kwargs)

# 	def __str__(self):
# 		return f'{self.user.username} BioData'


class Profile(models.Model):
	user = models.OneToOneField(User, default=None, null=True, on_delete=models.CASCADE)
	image = models.ImageField(default='default.png', upload_to='profile_pics')

	def __str__(self):
		return f'{self.user.username} Profile'


class OthersProfiles(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	slug = models.SlugField(unique=True)

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		self.slug = slugify(self.user.username)
		super(OthersProfiles, self).save(*args, **kwargs)
	
	def get_absolute_url(self):
		return reverse('otherprofiles', kwargs={'slug': self.slug })


class Gallery(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	def image_directory_path(instance, filename):
		return f'user_{instance.user.id}/{filename}'
	gallery_image = models.ImageField(upload_to=image_directory_path, default="image.png")

	def __str__(self):
		return f'{self.user.username} Gallery'


class UserMoreInfoModel(models.Model):
	HOBBIES = [
	('Reading', 'Reading'), ('Watching TV', 'Watching TV'), ('Family Time', 'Family Time'), 
	('Going to Movies', 'Going to Movies'), ('Fishing', 'Fishing'), ('Computer', 'Computer'), 
	('Gardening', 'Gardening'), ('Walking', 'Walking'), ('Exercise', 'Exercise'), 
	('Listening to Music', 'Listening to Music'), ('Entertaining', 'Entertaining'), 
	('Hunting', 'Hunting'), ('Team Sports', 'Team Sports'), ('Shopping', 'Shopping'), 
	('Traveling', 'Traveling'), ('Sleeping', 'Sleeping'), ('Socializing', 'Socializing'), 
	('Sewing', 'Sewing'), ('Church Activities', 'Church Activities'), ('Relaxing', 'Relaxing'), 
	('Playing Music', 'Playing Music'), ('Housework', 'Housework'), ('Crafts', 'Crafts'), 
	('Watching Sports', 'Watching Sports'), ('Bicycling', 'Bicycling'), ('Playing Cards', 'Playing Cards'), 
	('Cooking', 'Cooking'), ('Swimming', 'Swimming'), ('Camping', 'Camping'), ('Writing', 'Writing'), 
	('Animal Care', 'Animal Care'), ('Painting', 'Painting'), ('Running', 'Running'), ('Dancing', 'Dancing'), 
	('Tennis', 'Tennis'), ('Theater', 'Theater'), ('Beach', 'Beach'), 
	('Volunteer Work', 'Volunteer Work')
	]

	CHOICES_YESorNO = [
	(0, 'Yes'),
	(1, 'No')
	]

	CH2 = [
	('Non-smoker', 'Non-smoker'), 
	('Occasional smoker', 'Occasional smoker'), 
	('Smoker', 'Smoker')
	]
	
	CH3 = [
		('Never', 'Never'), 
		('On special occasion', 'On special occasion'), 
		('Once a week', 'Once a week'), 
		('Few times a week', 'Few times a week'), 
		('Daily', 'Daily')
		]

	MUSIC = [
	    ('rap', 'rap'), ('gospel', 'gospel'),
	    ('jazz', 'jazz'), ('blues/soul', 'blues/soul'),
	    ('hip-hop', 'hip-hop'), ('oldies', 'oldies'),
	    ('classical', 'classical'), ('R&B', 'R&B'),
	    ('reggae', 'reggae'), ('others', 'others')
	    ]

	SPORT = [
	    ('volleyball', 'volleyball'), ('badminton', 'badminton'), 
	    ('running', 'running'), ('basketball', 'basketball'), 
	    ('gymnastics', 'gymnastics'), ('table tennis', 'table tennis'),
	    ('handball', 'handball'), ('football', 'football'),
	    ('martial arts', 'martial arts'), ('squash', 'squash'), 
	    ('other', 'other')
	    ]

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	hobby                     = ListField(max_length= 300,)
	do_you_take_alcohol       = models.CharField(max_length= 500, choices=CH3, default="Never")
	do_you_smoke              = models.CharField(max_length= 500, choices=CH2, default="Non-smoker")
	sport                     = ListField(max_length= 300)
	music                     = ListField(max_length= 300)

	def __str__(self):
		return f'{self.user.username} Hobbies'


class BioDataModel(models.Model):
	HEIGHT = [
	('< 60inches(152.40cm)', '< 60inches(152.40cm)'),
	('> 60inches(152.40cm) but < 65inches(165.10cm)', '> 60inches(152.40cm) but < 65inches(165.10cm)'),
	('> 65inches(165.10cm) but < 70inches(177.80cm)', '> 65inches(165.10cm) but < 70inches(177.80cm)'), 
	('> 70inches(177.80) but < 75inches(190.50cm)', '> 70inches(177.80) but < 75inches(190.50cm)'),
	('> 75inches(190.50cm) but < 80inches(203.20cm)', '> 75inches(190.50cm) but < 80inches(203.20cm)'),
	('> 80inches(203.20cm) but < 85inches(215.90cm)', '> 80inches(203.20cm) but < 85inches(215.90cm)'),
	('> 85inches(215.90cm) but < 90inches(228.6)', '> 85inches(215.90cm) but < 90inches(228.6cm)'),
	('> 90inches(228.6cm)', '> 90inches(228.6cm))')
	]


	COMPLEXION = [
	    ('very light', 'very light'),
	    ('light', 'light'),
	    ('brown/chocolate',
	    'brown/chocolate'),
	    ('dark brown', 'dark brown'),
	    ('very dark', 'very dark')
	    ]


	HAIR_COLOR = [
	('light', 'light'),
	('brown', 'brown'),
	('black', 'black')
	]

	RELIGION_CH = [
	('christainity', 'christainity'),
	('islam', 'islam'),
	('traditional', 'traditional'),
	('atheist', 'atheist')
	]

	SEX = [
	('male', 'male'),
	('female', 'female')
	]

	user  = models.OneToOneField(User, on_delete=models.CASCADE)
	height = models.CharField(max_length= 100, choices=HEIGHT)
	    
	eye_color = models.CharField(max_length= 100, choices=HAIR_COLOR)

	hair_color = models.CharField(max_length= 100, choices=HAIR_COLOR)
	complexion = models.CharField(max_length= 100, choices=COMPLEXION)

	date_of_birth = models.DateField()
	age = models.IntegerField()
	sex = models.CharField(max_length= 100, choices=SEX)
	religion = models.CharField(max_length= 100, choices=RELIGION_CH)
	
	institution = models.CharField(max_length=100, default="Funaab")
	describe = models.CharField(max_length=100)

	def save(self, *args, **kwargs):
		if self.date_of_birth.month > datetime.date.today().month:
			self.age = datetime.date.today().year - self.date_of_birth.year
		else:
			self.age = (datetime.date.today().year - self.date_of_birth.year) - 1 

		super(BioDataModel, self).save(*args, **kwargs)

	def __str__(self):
		return f'{self.user.username} BioData'

