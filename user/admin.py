from django.contrib import admin

# Register your models here.
from .models import (Hobby, UserMoreInfoModel, 
	Profile, BioDataModel,
	OthersProfiles, Gallery,
	
	)

admin.site.register(Hobby)
admin.site.register(UserMoreInfoModel)
admin.site.register(Profile)
admin.site.register(OthersProfiles)
admin.site.register(BioDataModel)
admin.site.register(Gallery)



