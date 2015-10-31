from django.test import TestCase
from classes.models import Class, Attendee
from django.contrib.auth.models import User
import datetime

# Create your tests here.
class ConflictTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='user a')
        Attendee.objects.create(user=user)
        print('creating classes')
        Class.objects.create(name='class a', start=datetime.datetime.strptime('11-14-2015 '+'1'+':'+'00', '%m-%d-%Y %H:%M'), end=datetime.datetime.strptime('11-14-2015 '+'2'+':'+'00', '%m-%d-%Y %H:%M'), max_attendees=20, teacher='', description='', quote='', information='', subtitle='')
        Class.objects.create(name='class b', start=datetime.datetime.strptime('11-14-2015 '+'2'+':'+'30', '%m-%d-%Y %H:%M'), end=datetime.datetime.strptime('11-14-2015 '+'3'+':'+'30', '%m-%d-%Y %H:%M'), max_attendees=20, teacher='', description='', quote='', information='', subtitle='')
        Class.objects.create(name='class c', start=datetime.datetime.strptime('11-14-2015 '+'3'+':'+'00', '%m-%d-%Y %H:%M'), end=datetime.datetime.strptime('11-14-2015 '+'4'+':'+'00', '%m-%d-%Y %H:%M'), max_attendees=20, teacher='', description='', quote='', information='', subtitle='')

    def test_conflict(self):
        print('testing')
        classa = Class.objects.get(name='class a')
        classb = Class.objects.get(name='class b')
        classc = Class.objects.get(name='class c')
        user = User.objects.get(username='user a')
        classa.signup(user=user)
        two = datetime.timedelta(hours=2)
        print(classa.start)
        print(classb.start)
        print(classc.start)
        print(classa.start-two)
        print(classb.start-two)
        print(classc.start-two)
        print(classc.start > classa.start)
        self.assertTrue(classa.is_conflict(classb))
        self.assertFalse(classa.is_conflict(classc))
        self.assertTrue(classb.is_conflict(classa))
        self.assertFalse(classc.is_conflict(classa))
        self.assertTrue(classb.is_conflict(classc))
        self.assertTrue(classc.is_conflict(classb))

    def test_signup(self):
        classa = Class.objects.get(name='class a')
        classb = Class.objects.get(name='class b')
        classc = Class.objects.get(name='class c')
        user = User.objects.get(username='user a')
        classa.signup(user=user)
        classb.signup(user=user)
        classc.signup(user=user)
