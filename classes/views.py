from django.shortcuts import render
from classes.models import Class

# Create your views here.
def index(request):
    # the index of the class listing, not of the website
    classes = Class.objects.all().order_by('start')
    return render(request, 'templates/class_index.html', {'classes': classes})