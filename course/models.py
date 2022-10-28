from email.policy import default
from pyexpat import model
from django.db import models

from accounts.models import Account
from payment.models import Order

# Create your models here.

class Course(models.Model):
    course_name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 100, unique = True)
    description = models.TextField(max_length = 1000, blank = True)
    course_image = models.ImageField(upload_to = 'photos/courses/', blank = True, null = True)

    course_price = models.IntegerField(default = 0)
    released = models.BooleanField(default = False)

    #For pricing cards
    course_feature_1 = models.CharField(max_length = 100, blank = True, null = True)
    course_feature_2 = models.CharField(max_length = 100, blank = True, null = True)
    course_feature_3 = models.CharField(max_length = 100, blank = True, null = True)

    # For course advertising
    catchy_intro = models.CharField(max_length = 100, default = 'Catchy Intro')
    catchy_description = models.CharField(max_length = 500, blank = True, null = True)
    instructor_name = models.CharField(max_length = 80, default = 'Abiduzzaman Abid')
    enrolled_students = models.IntegerField(default = 0)
    number_of_classes = models.IntegerField(default = 0)
    total_video_duration = models.CharField(max_length = 50 ,default = '-')

    # For purchased users

    def __str__(self):
        return self.course_name


class LearningPoint(models.Model):
    point = models.CharField(max_length = 50)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)

    def __str__(self):
        return self.course.course_name + ' - ' + self.point


class IncludedPoint(models.Model):
    point = models.CharField(max_length = 80)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)

    def __str__(self):
        return self.course.course_name + ' - ' + self.point


class Unit(models.Model):
    unit_name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 100)
    unit_price = models.IntegerField(default = 0)
    course = models.ForeignKey(Course, on_delete = models.SET_NULL, blank = True, null = True)

    def __str__(self): 
        return self.course.course_name + ' - ' + self.unit_name


class Chapter(models.Model):
    chapter_name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 100)

    unit = models.ForeignKey(Unit, on_delete = models.SET_NULL, blank = True, null = True)

    lecture_note = models.FileField(upload_to = 'notes/', blank = True, null = True)

    def __str__(self):
        return self.unit.unit_name + ' - ' + self.chapter_name


class Video(models.Model):
    video_name = models.CharField(max_length = 150)
    slug = models.SlugField(max_length = 150)
    video_description = models.TextField(max_length = 500, blank = True, null = True)
    video_url = models.CharField(max_length = 150)
    video_duration = models.IntegerField(default = 0, blank = True, null = True)
    date_updated = models.DateTimeField(auto_now= True)

    chapter = models.ForeignKey(Chapter, on_delete = models.SET_NULL, blank = True, null = True)


class Subscription(models.Model):
    subscription_type = models.IntegerField(default = 0)
    course = models.ForeignKey(Course, on_delete = models.SET_NULL, blank = True, null = True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, blank = True, null = True)
    user = models.ForeignKey(Account, on_delete = models.CASCADE)
    active = models.BooleanField(default = False)

    ### For manual approval
    manually_approved = models.BooleanField(default = False)
    description = models.TextField(max_length = 250, blank = True, null = True)

    ### Otherwise, it is related to this order
    order = models.ForeignKey(Order, on_delete = models.CASCADE, blank = True, null = True)

    @property
    def is_active(self):
        return self.manually_approved or self.order.status == 'A'

    # def __str__(self):
    #     if self.subscription_type == 0:
    #         show = self.user.username + '|' + self.course.course_name + ' -- Full Course'
    #     elif self.subscription_type == 1:
    #         show = self.user.username + '|' + self.unit.course.course_name + ' -- ' + self.unit.unit_name
        
    #     if self.is_active():
    #         show += '| Active'
    #     else:
    #         show += '| Inactive'


class About(models.Model):
    website_name = models.CharField(max_length = 100, default = 'Abids Tutorials')
    about_title = models.CharField(max_length = 100, default = 'Abids Tutorials')
    about_us = models.TextField(max_length = 500, blank = True, null = True)
    contact_number = models.CharField(max_length = 20, blank = True, null = True)
    contact_email = models.CharField(max_length = 50, blank = True, null = True)
    facebook_link = models.CharField(max_length = 80, blank = True, null = True)
    twitter_link = models.CharField(max_length = 80, blank = True, null = True)
    instagram_link = models.CharField(max_length = 80, blank = True, null = True)

