from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.db import IntegrityError
import re


class Class(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField()
    attendees = models.ManyToManyField('Attendee')
    start = models.DateTimeField()
    end = models.DateTimeField()
    max_attendees = models.IntegerField(default=20)
    teacher = models.CharField(max_length=64)
    description = models.TextField()
    quote = models.TextField(max_length=128)
    manual_live = models.BooleanField(default=False)
    information = models.TextField()
    subtitle = models.CharField(max_length=128)

    def is_conflict(self, other_class):
        two = datetime.timedelta(hours=2)
        if self.start < other_class.start:
            return self.start > other_class.start - two
        if self.start > other_class.start:
            return self.start < other_class.start + two

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def signup(self, user):
        if len(self.attendees.all()) < self.max_attendees:
            self.attendees.add(user.attendee)
        else:
            try:
                WaitlistedAttendee.objects.create(clss=self, user=user)
            except IntegrityError:
                raise

    class Meta:
        ordering = ['start']

    def __str__(self):
        return self.name

    def image_name(self):
        return re.sub('[\W_]+', '', self.name).lower()

    def start_time(self):
        return self.start.time().strftime("%I:%M %p")

    def end_time(self):
        return self.end.time().strftime("%I:%M %p")

    def is_live(self):
        return self.start < timezone.now() < self.end or self.manual_live


class Attendee(models.Model):
    user = models.OneToOneField(User)

    def is_eligible(self, new_class):
        classes = self.class_set.all()
        if not any([cls.is_conflict(new_class) for cls in classes]) and classes.length <= 3:
            return True
        return False


class WaitlistedAttendee(models.Model):
    clss = models.ForeignKey(Class)
    user = models.ForeignKey(User)
    signed_up = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.signed_up = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['signed_up']
        unique_together = ('clss', 'user')
