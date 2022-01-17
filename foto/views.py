from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from .forms import ImageForm
from .models import Image
import os
from pathlib import Path


# Create your views here.

def index(request):
    imageform = ImageForm()
    images_a = Image.objects.all()
    return render(request, 'index.html', {"form": imageform,  'images': images_a})

def upload(request):
    imageform = ImageForm()
    images_a = Image.objects.all()
    return render(request, 'upload.html', {"form": imageform,  'images': images_a})


def image_upload_view(request):
    """Process images uploaded by users"""
    images = Image.objects.all()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'upload.html', {'form': form, 'img_obj': img_obj, 'images': images})
    else:
        form = ImageForm()
    return render(request, 'index.html', {'form': form})

def edit(request):
    images_a = Image.objects.all()
    return render(request, 'edit.html', {'images': images_a})

def delete(request, id):
    try:
        image = Image.objects.get(id=id)
        image_path = os.path.realpath("media\\" + str(image.image))
        os.remove(image_path)
        image.delete()
        return HttpResponseRedirect("/edit/")
    except Image.DoesNotExist:
        return HttpResponseNotFound("<h2>Image not found</h2>")

def likes(request, id):
        like = Image.objects.get(id=id)
        like.likes += 1
        like.save()
        return HttpResponseRedirect("/")