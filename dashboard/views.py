from django.contrib import messages, auth
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import UserProfile

from course.models import Chapter, Course, Subscription, Unit, Video
from dashboard.models import Dislike, Like, Watchlater, Comment, Reply
from django.contrib.auth.decorators import login_required

# Create your views here.


def subscribed_to_course(user, course):
    try:
        subscription = Subscription.objects.get(user = user, course = course, active = True)
        return True
    except:
        return False

def subscribed_to_unit(user, unit):
    try:
        subscription = Subscription.objects.get(user = user, unit = unit, active = True)
        return True
    except:
        return False

def get_relevant_courses(user):
    courses = Course.objects.filter(released = True)
    relevant_courses = []
    for course in courses:
        ok = False
        if Subscription.objects.filter(user = user, course = course, active = True).count() > 0:
            ok = True
        for unit in course.unit_set.all():
            if Subscription.objects.filter(user = user, unit = unit, active = True).count() > 0:
                ok = True
        if ok:
            relevant_courses.append(course)
    return relevant_courses


def user_has_access_unit(user, unit):
    course = unit.course
    if Subscription.objects.filter(user = user, course = course, active = True).count() > 0 or Subscription.objects.filter(user = user, unit = unit, active = True).count() > 0:
        return True
    else:
        return False


def get_first_subscribed_unit(user, course):
    first_unit = None
    for unit in course.unit_set.all():
        if user_has_access_unit(user, unit):
            first_unit = unit
    return first_unit


def get_all_subscribed_units(user, course):
    units = []
    for unit in course.unit_set.all():
        if user_has_access_unit(user, unit):
            units.append(unit)
    return units

def first_chapter_of_unit(unit):
    chapters = unit.chapter_set.all()
    if chapters.count() > 0:
        return chapters[0]
    else:
        return None

def first_video_of_chapter(chapter):
    videos = chapter.video_set.all()
    if videos.count() > 0:
        return videos[0]
    else:
        return None

def get_slugs_from_video_id(video_id):
    try:
        video = Video.objects.get(id = video_id)
    except:
        return False
    
    video_slug = video.id
    chapter_slug = video.chapter.slug
    unit_slug = video.chapter.unit.slug
    course_slug = video.chapter.unit.course.slug

    return {
        'video_slug' : video_slug, 
        'chapter_slug' : chapter_slug,
        'unit_slug' : unit_slug,
        'course_slug' : course_slug,
    }

def user_has_access_to_video(user, video):
    try:
        slugs = get_slugs_from_video_id(video.id)
        unit = Unit.objects.get(slug = slugs['unit_slug'])
        return user_has_access_unit(user, unit)
    except:
        return False

@login_required
def dashboard_video(request, *args, **kwargs):
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        course_slug = kwargs['course_slug']
        course = Course.objects.get(slug = course_slug)
        unit_slug = kwargs['unit_slug']
        unit = Unit.objects.get(slug = unit_slug)
        chapter_slug = kwargs['chapter_slug']
        chapter = Chapter.objects.get(slug = chapter_slug)
        video_slug = kwargs['video_slug']
        video = Video.objects.get(id = video_slug)

        left_menu = {}
        for _unit in course.unit_set.all():
            left_menu[_unit.unit_name] = {
                'unit': _unit,
                'no_access': True,
            }
            if user_has_access_unit(request.user, _unit):
                left_menu[_unit.unit_name]['no_access'] = False
        print(left_menu)

        if user_has_access_to_video(request.user, video):
            likes_count = Like.objects.filter(video__id = video.id).count()
            dislikes_count = Dislike.objects.filter(video__id = video.id).count()
            is_watched_later = False
            
            if Watchlater.objects.filter(video__id = video.id, user = request.user).count() > 0:
                is_watched_later = True
            comments = Comment.objects.filter(video__id = video.id)
                        
            context = {
                'course': course,
                'unit': unit,
                'chapter': chapter,
                'video': video,
                'likes_count': likes_count,
                'dislikes_count': dislikes_count,
                'is_watched_later': is_watched_later,
                'comments': comments,
                'user_profile': user_profile,
                'dashboard_page': True,
                'left_menu': left_menu,
            }
        else:
            context = {
                'course': course,
                'unit': unit,
                'chapter': chapter,
                'video': video,
                'likes_count': 0,
                'dislikes_count': 0,
                'is_watched_later': False,
                'comments': None,
                'user_profile': user_profile,
                'dashboard_page': True,
                'no_access': True,
                'left_menu': left_menu,
            }
        return render(request, 'dashboard/course.html', context)

    except:
        return redirect('profile')


@login_required
def dashboard_chapter(request, *args, **kwargs):
    try:
        course_slug = kwargs['course_slug']
        course = Course.objects.get(slug = course_slug)
        unit_slug = kwargs['unit_slug']
        unit = Unit.objects.get(slug = unit_slug)
        chapter_slug = kwargs['chapter_slug']
        chapter = Chapter.objects.get(slug = chapter_slug)
        video = first_video_of_chapter(chapter)
        return redirect('dashboard', course_slug = course_slug, unit_slug = unit.slug, chapter_slug = chapter.slug, video_slug = video.id)

    except:
        return redirect('dashboard')

@login_required
def dashboard_unit(request, *args, **kwargs):
    try:
        course_slug = kwargs['course_slug']
        course = Course.objects.get(slug = course_slug)
        unit_slug = kwargs['unit_slug']
        unit = Unit.objects.get(slug = unit_slug)
        chapter = first_chapter_of_unit(unit)
        return redirect('dashboard', course_slug = course_slug, unit_slug = unit.slug, chapter_slug = chapter.slug)
    except:
        return redirect('dashboard')


@login_required
def dashboard_course(request, *args, **kwargs):
    try:
        course_slug = kwargs['course_slug']
        course = Course.objects.get(slug = course_slug)
        units = get_all_subscribed_units(request.user, course)
        has_subscription = False
        for unit in units:
            has_subscription = True
            ##  Checking if the unit has videos
            for chapter in unit.chapter_set.all():
                if chapter.video_set.all().count() > 0:
                    return redirect('dashboard', course_slug = course_slug, unit_slug = unit.slug, chapter_slug = chapter.slug)
        if not has_subscription:
            messages.warning(request, "You don't have any subscription for " + course.course_name + ". Please subscribe or browse from your dashboard")
            return redirect('dashboard')
        else:
            messages.warning(request, "No video has been uploaded yet. You will be notified once they are uploaded.")
            return redirect('dashboard')
    except:
        return redirect('dashboard')


@login_required
def dashboard_root(request, *args, **kwargs):
    try:
        relevant_courses = get_relevant_courses(request.user)
        
        nosubscription = False
        if len(relevant_courses) == 0:
            nosubscription = True
        context = {
            'relevant_courses': relevant_courses,
            'nosubscription': nosubscription,
        }
    
        return render(request, 'dashboard/dashboard_root.html', context = context)


    except:
        messages.error(request, "Error lodaing dashboard. Try again and inform us if this issue continues.")
        return redirect('profile')




def comment(request):
    if request.method == 'POST': 
        # try:
        comment_content = request.POST['comment_content']
        video = Video.objects.get(id = request.POST['video_id'])
        comment = Comment(comment_content = comment_content, video = video, user = request.user)
        comment.save()

        slugs = get_slugs_from_video_id(video.id)
        if slugs:
            return redirect('dashboard', course_slug = slugs['course_slug'], chapter_slug = slugs['chapter_slug'], unit_slug = slugs['unit_slug'], video_slug = slugs['video_slug'] )
        else:
            return redirect('profile')
        # except:
            # return redirect('profile')

    else:
        return redirect('profile')


def reply(request):
    if request.method == 'POST': 
        # try:
        print(request.POST)
        reply_content = request.POST['reply_content']
        comment = Comment.objects.get(id = request.POST['comment_id'])
        video = Video.objects.get(id = request.POST['video_id'])
        reply = Reply(reply_content = reply_content, reply_to = comment, user = request.user)
        reply.save()

        slugs = get_slugs_from_video_id(video.id)
        if slugs:
            return redirect('dashboard', course_slug = slugs['course_slug'], chapter_slug = slugs['chapter_slug'], unit_slug = slugs['unit_slug'], video_slug = slugs['video_slug'] )
        else:
            return redirect('profile')
        # except:
            # return redirect('profile')

    else:
        return redirect('profile')


@login_required
def like(request):
    if request.method == 'POST':
        # try:
        video = Video.objects.get(id = request.POST['video_id'])
        like = Like.objects.filter(video = video, user = request.user)
        if like.count() == 0:
            dislike = Dislike.objects.filter(video = video, user = request.user)
            if dislike.count() != 0: 
                dislike[0].delete()
            like = Like(video = video, user = request.user)
            like.save()

        slugs = get_slugs_from_video_id(video.id)
        if slugs:
            return redirect('dashboard', course_slug = slugs['course_slug'], chapter_slug = slugs['chapter_slug'], unit_slug = slugs['unit_slug'], video_slug = slugs['video_slug'] )
        else:
            return redirect('profile')
            
        # except:
        #     return redirect('dashboard')

    else:
        print("BALLLL\n\n\n\n")
        return redirect('dashboard')


@login_required
def dislike(request):
    if request.method == 'POST':
        print("FUCKERSSSS")
        try:
            video = Video.objects.get(id = request.POST['video_id'])
            dislike = Dislike.objects.filter(video = video, user = request.user)
            
            if dislike.count() == 0:
                like = Like.objects.filter(video = video, user = request.user)
                if like.count() != 0: 
                    like[0].delete()
                dislike = Dislike(video = video, user = request.user)
                dislike.save()

            slugs = get_slugs_from_video_id(video.id)
            
            if slugs:
                return redirect('dashboard', course_slug = slugs['course_slug'], chapter_slug = slugs['chapter_slug'], unit_slug = slugs['unit_slug'], video_slug = slugs['video_slug'] )
            else:
                return redirect('profile')
            
        except:
            return redirect('dashboard')

    else:
        return redirect('dashboard')

@login_required
def addWatchLater(request):
    if request.method == 'POST':
        try:
            video = Video.objects.get(id = request.POST['video_id'])
            watchLater = Watchlater.objects.filter(video = video, user = request.user)
            if watchLater.count() == 0:
               watchLater = Watchlater(video = video, user = request.user)
               watchLater.save()


            slugs = get_slugs_from_video_id(video.id)
            if slugs:
                return redirect('dashboard', course_slug = slugs['course_slug'], chapter_slug = slugs['chapter_slug'], unit_slug = slugs['unit_slug'], video_slug = slugs['video_slug'] )
            else:
                return redirect('profile')
            
        except:
            return redirect('dashboard')

    else:
        return redirect('dashboard')


@login_required
def removeWatchLater(request):
    if request.method == 'POST':
        try:
            video = Video.objects.get(id = request.POST['video_id'])
            watchLater = Watchlater.objects.filter(video = video, user = request.user)
            if watchLater.count() > 0:
               watchLater[0].delete()
               
            slugs = get_slugs_from_video_id(video.id)
            if slugs:
                return redirect('dashboard', course_slug = slugs['course_slug'], chapter_slug = slugs['chapter_slug'], unit_slug = slugs['unit_slug'], video_slug = slugs['video_slug'] )
            else:
                return redirect('profile')
            
        except:
            return redirect('dashboard')

    else:
        return redirect('dashboard')