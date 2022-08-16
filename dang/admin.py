from django.contrib import admin
from .models import User, Post, Cafe, Place, Accomodation, Medical, Like

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    pass

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    pass

@admin.register(Accomodation)
class AccomodationAdmin(admin.ModelAdmin):
    pass

@admin.register(Medical)
class MedicalAdmin(admin.ModelAdmin):
    pass

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass