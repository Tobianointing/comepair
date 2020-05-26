from django.contrib import admin

# Register your models here.
from .models import (UserMoreInfoModel, 
	Profile, BioDataModel,
	OthersProfiles, Gallery,GalleryNew
	
	)

admin.site.register(UserMoreInfoModel)
admin.site.register(Profile)
admin.site.register(OthersProfiles)
admin.site.register(BioDataModel)
admin.site.register(Gallery)
admin.site.register(GalleryNew)


