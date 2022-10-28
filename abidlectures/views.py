from django.shortcuts import render
from course.models import Course, About

def home(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, 'home.html', context)


def about(request):
    about = About.objects.all()
    if about.count() > 0:
        context = {
            'about' : about[0],
        }
    else:
        context = {
            'about': None,
        }
    return render(request, 'about.html', context)