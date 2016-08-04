from django import forms
from galleries.models import Photo


class PhotoForm(forms.ModelForm):
    

    class Meta:
        model = Photo
        exclude = ['file_small', 'file_thumbnail', 'base_height', 'base_width']
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 3, 'cols': 15})
        }
