from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Class(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField()
    attendee = models.ManyToManyField(Attendee)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def is_conflict(self, other_class):
        return (self.start < other_class.end) and (self.end > other_class.start)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Class, self).save(*args, **kwargs)


class Attendee(models.Model):
    user = models.ForeignKey(User)

    def is_eligible(self, new_class):
        classes = self.class_set.all()
        if not any([cls.is_conflict(new_class) for cls in classes]) and classes.length <= 3:
            return True
