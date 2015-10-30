from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from classes.models import Class, Attendee
from classes.forms import ClassForm, SignupForm
from classes.decorators import staff_member_required
import datetime


def index(request):
    # the index of the class listing, not of the website
    classes = Class.objects.all().order_by('start')
    return render(request, 'templates/masterclass-list.html', {'classes': classes})


def drop(request, class_pk, user_pk):
    if user_pk != request.user.pk or request.user.is_staff:
        class_ = get_object_or_404(Class, pk=class_pk)
        class_.attendees.remove(User.objects.get(pk=user_pk).attendee)
    return redirect('classes.views.detail', class_pk=class_pk)


@staff_member_required
def toggle_live(request, class_pk):
    class_ = get_object_or_404(Class, pk=class_pk)
    if class_.manual_live:
        class_.manual_live = False
    else:
        class_.manual_live = True

    return redirect(add_or_edit_class)


@staff_member_required
def delete_class(request, class_pk):
    class_ = get_object_or_404(Class, pk=class_pk)
    class_.delete()
    return redirect(add_or_edit_class)


def detail(request, class_pk):
    Attendee.objects.get_or_create(user=request.user)  # Hackish but idk what else to do
    class_ = get_object_or_404(Class, pk=class_pk)
    form = SignupForm(initial={'userpk': request.user.pk, 'classpk': class_pk})
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            class_.signup(user=request.user)
            return redirect('classes.views.detail', class_pk=class_.pk)

    context = {
        'class': class_,
        'form': form,
    }
    return render(request, 'templates/masterclass-detail.html', context)


@staff_member_required
def add_or_edit_class(request, class_pk=None):

    if class_pk:
        clss = get_object_or_404(Class, pk=class_pk)
    else:
        clss = Class()

    if request.method == 'POST':
        form = ClassForm(request.POST, instance=clss)
        if form.is_valid():
            clss.start = datetime.datetime.strptime('11-14-2015 '+request.POST.get('start_time')+':'+request.POST.get('start_min'), '%m-%d-%Y %H:%M')
            clss.end = datetime.datetime.strptime('11-14-2015 '+request.POST.get('end_time')+':'+request.POST.get('end_min'), '%m-%d-%Y %H:%M')
            form.save()
            clss.save()
            return redirect(add_or_edit_class)

    form = ClassForm(instance=clss)
    classes = Class.objects.all()
    context = {
        'form': form,
        'classes': classes,
    }

    return render(request, 'templates/manage_classes.html', context)
