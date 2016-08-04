from django.shortcuts import render, get_object_or_404

from django.utils.translation import ugettext as _

from .models import Gallery, Photo

# Create your views here.


def gallery_list(request):
    gallery_list = Gallery.objects.order_by('-date')
    context = {
        'gallery_list': gallery_list
    }
    return render(request, 'galleries/index.html', context)


def gallery_detail(request, gallery_id):
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    context = {
        'gallery': gallery,
    }
    return render(request, 'galleries/detail.html', context)
