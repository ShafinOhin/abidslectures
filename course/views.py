from django.shortcuts import render
from .models import Course

# Create your views here.

def explore(request):
    courses = Course.objects.all()
    context = {
        'courses' : courses,
    }
    return render(request, 'course/explore.html', context)


def pricing(request):
    all_courses = Course.objects.filter(released = True)
    courses = {}
    flag = False
    for course in all_courses:
        courses[flag] = course
        if flag:
            flag = False
        else:
            flag = True

    context = {
        'courses' : courses,
    }
    return render(request, 'course/pricing.html', context)


def course_details(request, course_slug):
    course = Course.objects.get(slug = course_slug)
    context = {
        'course': course,
    }
    return render(request, 'course/course_details.html', context)