from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone


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

    def is_conflict(self, other_class):
        return (self.start < other_class.end) and (self.end > other_class.start)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def signup(self, user):
        if len(self.attendees.all()) < self.max_attendees:
            self.attendees.add(user.attendee)
        else:
            WaitlistedAttendee.objects.create(clss=self, user=user)

    class Meta:
        ordering = ['start']

    def __str__(self):
        return self.name

    def image_name(self):
        return self.name.replace(' ', '').lower()

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
    unique_together = (clss, user)

    def save(self, *args, **kwargs):
        if not self.id:
            self.signed_up = timezone.now()
        return super().save(*args, **kwargs)
