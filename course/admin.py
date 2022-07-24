from django.contrib import admin
from .models import Course, Subscription, Unit, Chapter, Video, About, IncludedPoint, LearningPoint


class LearningPointInline(admin.TabularInline):
    model = LearningPoint
    list_display = ['point']

class IncludedPointInline(admin.TabularInline):
    model = IncludedPoint
    list_display = ['point']


class CourseAdmin(admin.ModelAdmin):
    inlines  = [LearningPointInline, IncludedPointInline]
    prepopulated_fields = {'slug': ('course_name', )}
    list_display = ('course_name', 'slug')

class UnitAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('unit_name', )}
    list_display = ('unit_name', 'slug')

class ChapterAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('chapter_name', )}
    list_display = ('chapter_name', 'slug')

class VideoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('video_name', )}
    list_display = ('video_name', 'slug')

admin.site.register(Course, CourseAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Video, VideoAdmin)

admin.site.register(About)
admin.site.register(Subscription)