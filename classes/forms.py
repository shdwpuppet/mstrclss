from django.forms import ModelForm
from classes.models import Class

class ClassForm(ModelForm):

    class Meta:
        model = Class
        fields = ['name', 'teacher', 'max_attendees']