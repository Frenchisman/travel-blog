from django.contrib import admin
from django.contrib.sites.models import Site
# Register your models here.
from .models import Gallery, Photo
from galleries.forms.admin.forms import PhotoForm


class PhotoInline(admin.TabularInline):
    model = Photo
    form = PhotoForm
    extra = 1


class GalleryAdmin(admin.ModelAdmin):

    fields = ['title', 'description', 'date']
    inlines = [PhotoInline]

    class Media:
        css = {"all": ("galleries/css/admin/hide_admin_original.css",)}
        #  Hide original object column in admin interface to gain space.
admin.site.register(Gallery, GalleryAdmin)
# admin.site.unregister(Site)  # @TODO put this in another admin.py
