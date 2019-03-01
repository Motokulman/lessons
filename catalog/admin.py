from django.contrib import admin
from catalog.models import Genre, Language, Serial, Logia, Technology, Producer, CourseType, Video, Course, Lesson, Algorithm, Pupil, Country
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin

admin.site.register(Genre)
admin.site.register(Country)
admin.site.register(Language)
admin.site.register(Serial)
admin.site.register(Technology)
admin.site.register(Producer)
#admin.site.register(CourseType)
admin.site.register(Video)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Algorithm)
admin.site.register(Pupil)
admin.site.register(Logia)

#class CustomMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
 #   mptt_level_indent = 20
#admin.site.register(CourseType, MPTTModelAdmin) # For tree data storing
admin.site.register(
    CourseType,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)

     #       languages = CourseType.objects.create(name="Languages")
#       games = CourseType.objects.create(name="Games")
#       CourseType.objects.create(name="Not native language", parent=languages)
#       CourseType.objects.create(name="Native language", parent=languages)
#       CourseType.objects.create(name="Chess", parent=games)
#       CourseType.objects.create(name="Checkers", parent=games)


