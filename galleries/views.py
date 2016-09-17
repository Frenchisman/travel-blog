from django.shortcuts import render, get_object_or_404

from django.utils.translation import ugettext as _

import random
from .models import Gallery, Photo

# Create your views here.


def gallery_list(request):
    gallery_list = Gallery.objects.order_by('-date')

    #Add a random photo to context to display on gallery list page.



    context = {
        'gallery_list': gallery_list,
    }

    photo_list = Photo.objects.all()
    if(len(photo_list) != 0):
        random_photo = photo_list[random.randint(0, len(photo_list)-1)]
        context.update({'random_photo':random_photo,})

    return render(request, 'galleries/index.html', context)


def gallery_detail(request, gallery_id):
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    context = {
        'gallery': gallery,
    }
    return render(request, 'galleries/detail.html', context)
