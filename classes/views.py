from django.shortcuts import render, get_object_or_404
from classes.models import Class

# Create your views here.
def index(request):
    # the index of the class listing, not of the website
    classes = Class.objects.all().order_by('start')
    return render(request, 'templates/class_index.html', {'classes': classes})

def detail(request, class_pk):
    class_ = get_object_or_404(Class, pk=class_pk)
    return render(request, 'templates/class_detail.html', {'class': class_})
