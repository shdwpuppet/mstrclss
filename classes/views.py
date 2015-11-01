from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from classes.models import Class, WaitlistedAttendee
from classes.forms import ClassForm, SignupForm
from django.contrib.auth import logout
from classes.decorators import staff_member_required
import datetime
from django.http import HttpResponseRedirect
from django.db import IntegrityError


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def index(request, user=False):
    # the index of the class listing, not of the website
    if user:
        classes = Class.objects.all().order_by('start')
    else:
        classes = request.user.attendee.class_set.all()
    return render(request, 'templates/masterclass-list.html', {'classes': classes})


def drop(request, class_pk, user_pk):
    if user_pk != request.user.pk or request.user.is_staff:
        class_ = get_object_or_404(Class, pk=class_pk)
        class_.attendees.remove(User.objects.get(pk=user_pk).attendee)
        class_.wl_moveup()
    return redirect('classes.views.detail', class_pk=class_pk)


def wl_drop(request, class_pk, user_pk):
    if user_pk == request.user.pk or request.user.is_staff:
        wlatt = get_object_or_404(WaitlistedAttendee, clss__pk=class_pk, user__pk=user_pk)
        wlatt.delete()
    return redirect('classes.views.detail', class_pk=class_pk)


@staff_member_required()
def wl_moveup(request, class_pk):
    get_object_or_404(Class, pk=class_pk).wl_moveup()
    return redirect(add_or_edit_class)

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


def schedule(request):
    classes = Class.objects.all()
    return render(request, 'templates/schedule.html', {'classes': classes})


def detail(request, class_pk):
    class_ = get_object_or_404(Class, pk=class_pk)
    form = SignupForm(initial={'userpk': request.user.pk, 'classpk': class_pk})
    first_class = False
    if not request.user.is_anonymous():
        if request.user.attendee.class_set.all().count() == 0:
            first_class = True
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                class_.signup(user=request.user)
            except IntegrityError:
                messages.error(request, 'You are already waitlisted')
            return redirect('classes.views.detail', class_pk=class_.pk)
    waitlist = WaitlistedAttendee.objects.filter(clss=class_)
    is_waitlisted = waitlist.filter(user=request.user).exists()
    context = {
        'class': class_,
        'form': form,
        'first_class': first_class,
        'waitlist': waitlist,
        'is_waitlisted': is_waitlisted,
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
            clss.wl_moveup()
            return redirect(add_or_edit_class)

    form = ClassForm(instance=clss)
    classes = Class.objects.all()
    context = {
        'form': form,
        'classes': classes,
    }

    return render(request, 'templates/manage_classes.html', context)
