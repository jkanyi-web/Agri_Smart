from django.contrib import admin
from .models import Crop, ForumPost, ForumComment, CropListing, TransactionRecord, UserProfile

admin.site.register(Crop)
admin.site.register(ForumPost)
admin.site.register(ForumComment)
admin.site.register(CropListing)
admin.site.register(TransactionRecord)
admin.site.register(UserProfile)
