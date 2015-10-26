from django.shortcuts import render, get_object_or_404, redirect
from classes.models import Class
from django.core.exceptions import ValidationError
from classes.forms import ClassForm
from classes.decorators import staff_member_required


def index(request):
    # the index of the class listing, not of the website
    classes = Class.objects.all().order_by('start')
    return render(request, 'templates/masterclass-list.html', {'classes': classes})


def detail(request, class_pk):
    class_ = get_object_or_404(Class, pk=class_pk)
    return render(request, 'templates/class_detail.html', {'class': class_})


def signup(request, class_pk):
    clss = get_object_or_404(Class, pk=class_pk)
    try:
        clss.signup(user=request.user)
    except ValidationError as error:
        if error.code == "unique_together":
            print("attempted to signup for a class already signed up for")


@staff_member_required
def add_or_edit_class(request, class_pk=None):

    if class_pk:
        clss = get_object_or_404(Class, pk=class_pk)
    else:
        clss = Class()

    if request.method == 'POST':
        form = ClassForm(request.POST, instance=clss)
        if form.is_valid():
            form.save()
            return redirect(add_or_edit_class)

    form = ClassForm(instance=clss)
    classes = Class.objects.all()
    context = {
        'form': form,
        'classes': classes,
    }

    return render(request, 'templates/manage_classes.html', context)
