import io
import uuid
import os
from PIL import Image as Img
from django.db import models
from datetime import date
from django.utils.translation import ugettext as _
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.


class Gallery(models.Model):
    title = models.CharField(
        _('Titre de la Galerie'), max_length=150)
    description = models.TextField(_('Description'), blank=True, null=True)
    date = models.DateField(_('Date'), default=date.today)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Galerie")
        verbose_name_plural = _("Galeries")


def content_filename(instance, filename):
    today = date.today()
    today_path = today.strftime("%Y/%m/%d/")
    path, ext = os.path.splitext(filename)
    return (
        'uploads/photos/normal/' +
        today_path +
        instance.title +
        "_" +
        uuid.uuid4().hex +
        ext)


def content_filename_small(instance, filename):
    today = date.today()
    today_path = today.strftime("%Y/%m/%d/")
    path, ext = os.path.splitext(filename)
    return (
        'uploads/photos/small/' +
        today_path +
        instance.title +
        "_" +
        uuid.uuid4().hex +
        ext)


def content_filename_thumbnail(instance, filename):
    today = date.today()
    today_path = today.strftime("%Y/%m/%d/")
    path, ext = os.path.splitext(filename)
    return (
        'uploads/photos/thumb/' +
        today_path +
        instance.title +
        "_" +
        uuid.uuid4().hex +
        ext)


class Photo(models.Model):
    title = models.CharField(_('Titre'), max_length=150, blank=True, null=True)
    caption = models.TextField(_('Légende'), blank=True, null=True)
    alt_text = models.CharField(
        _('Alternative Textuelle'), max_length=125, blank=True, null=True)
    file = models.ImageField(
        _('Fichier'),
        upload_to=content_filename,
        max_length=200,
    )
    file_small = models.ImageField(upload_to=content_filename_small, null=True)
    file_thumbnail = models.ImageField(
        upload_to=content_filename_thumbnail, null=True)
    base_height = models.IntegerField(default=100, blank=True)
    base_width = models.IntegerField(default=100, blank=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)

    def get_html_title(self):
        """
        Return the value for the title attribute of the photo in
        the html template

        If Title is not set, try to return the caption,
        If caption is not set, try to return the alt_text
        """
        if self.title:
            return self.title
        elif self.caption:
            return self.caption
        else:
            return self.alt_text

    def get_html_caption(self):
        """
        Return the value for the caption attribute of the photo in
        the html template

        If caption is not set, try to return the title,
        If title is not set, try to return the alt_text
        """
        if self.caption:
            return self.caption
        elif self.title:
            return self.title
        else:
            return self.alt_text

    def get_html_alt_text(self):
        """
        Return the value for the alt_text attribute of the photo in
        the html template

        If alt_text is not set, try to return the caption,
        If caption is not set, try to return the title
        """
        if self.alt_text:
            return self.alt_text
        elif self.caption:
            return self.caption
        else:
            return self.title

    def save(self, *args, **kwargs):
        if self.file:
            self.base_height = self.file.height
            self.base_width = self.file.width
            img = Img.open(io.BytesIO(self.file.read()))
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Convert the Base Image to JPEG without touching size.
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=70)
            output.seek(0)
            self.file = InMemoryUploadedFile(
                output, 'ImageField', "%s.jpg" % self.file.name.split('.')[0],
                'image/jpeg', output.seek(0, os.SEEK_END), None)

            # Make a smaller image ( size/2 ) for lower resolutions
            output_small = io.BytesIO()
            img.thumbnail((
                self.file.width / 2,
                self.file.height / 2),
                Img.ANTIALIAS)
            img.save(output_small, format='JPEG', quality=70)
            output_small.seek(0)
            self.file_small = InMemoryUploadedFile(
                output_small, 'ImageField',
                "%s.jpg" % self.file.name.split('.')[0],
                'image/jpeg', output_small.seek(0, os.SEEK_END), None)

            # Make a thumbnail for list_display
            output_thumb = io.BytesIO()
            img.thumbnail((200, 200), Img.ANTIALIAS)
            img.save(output_thumb, format='JPEG', quality=70)
            output_thumb.seek(0)
            self.file_thumbnail = InMemoryUploadedFile(
                output_thumb, 'ImageField',
                "%s.jpg" % self.file.name.split('.')[0],
                'image/jpeg', output_thumb.seek(0, os.SEEK_END), None)

        super(Photo, self).save(*args, **kwargs)
