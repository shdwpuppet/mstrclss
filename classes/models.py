from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Class(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField()
    attendees = models.ManyToManyField('Attendee')
    start = models.DateTimeField()
    end = models.DateTimeField()
    max_attendees = models.IntegerField(default=20)

    def is_conflict(self, other_class):
        return (self.start < other_class.end) and (self.end > other_class.start)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Class, self).save(*args, **kwargs)

    def signup(self, attendee):
        if all([self.is_conflict(clss) for clss in attendee.class_set.all()]) and attendee not in self.attendees.all():
            if len(self.attendees.all()) < self.max_attendees:
                self.attendees.add(attendee)
            else:
                WaitlistedAttendee.objects.create()


class Attendee(models.Model):
    user = models.OneToOneField(User)
    def is_eligible(self, new_class):
        classes = self.class_set.all()
        if not any([cls.is_conflict(new_class) for cls in classes]) and classes.length <= 3:
            return True


class WaitlistedAttendee(models.Model):
    clss = models.ForeignKey(Class)
    user = models.ForeignKey(User)
    signed_up = models.DateTimeField()
    unique_together = (clss, user)
