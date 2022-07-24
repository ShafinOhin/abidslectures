from django.shortcuts import redirect, render

from course.models import Course

# Create your views here.

def course_dashboard(request, course_slug):
    try:
        course = Course.objects.get(slug = course_slug)
    except:
        return redirect('profile')
    
    context = {
        'course': course,
    }
    return render(request, 'dashboard/course.html', context)
