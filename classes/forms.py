from django.forms import ModelForm
from classes.models import Class
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class ClassForm(ModelForm):

    class Meta:
        model = Class
        fields = ['name', 'subtitle', 'information', 'teacher', 'max_attendees', 'description', 'quote']


class SignupForm(forms.Form):
    userpk = forms.IntegerField(widget=forms.HiddenInput())
    classpk = forms.IntegerField(widget=forms.HiddenInput())

    def clean(self):
        user = User.objects.get(pk=self.cleaned_data.get('userpk'))
        clss = Class.objects.get(pk=self.cleaned_data.get('classpk'))

        if any([clss.is_conflict(cls) for cls in user.attendee.class_set.all()]):
            raise ValidationError('This class time has a conflict with one or more classes you are currently signed up for')
        elif user.attendee in clss.attendees.all():
            raise ValidationError('You have already signed up for this class')

        return self.cleaned_data
