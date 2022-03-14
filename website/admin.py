from django.db import models
from website.models import College, Course, EducationDetails, Facility, Inquiry, Review, Stream, Testimonial, ExamDetail
from django.contrib import admin

# Register your models here.


class EducationDetailsAdmin(admin.ModelAdmin):
    list_display = ['user', 'degree', 'passing_year',
                    'university', 'score', 'stream']
    list_filter = ['user', 'degree', 'passing_year', 'university', 'stream']
    search_fields = ['user__email', 'degree',
                     'passing_year', 'university', 'score', 'stream']


class CollegeAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'college_type']
    list_filter = ['name', 'state', 'college_type']
    search_fields = ['name', 'city', 'state', 'college_type']

    prepopulated_fields = {'slug': ('name', 'city')}


class ExamDetailAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_year', 'exam_mode']
    list_filter = ['name', 'exam_year', 'stream', 'exam_mode']
    search_fields = ['name', 'exam_year', 'stream', 'exam_mode']

    prepopulated_fields = {'slug': ('name', 'exam_year')}

    def get_stream(self, obj):
        print(obj)
        return "\n".join([s.stream for s in obj.objects.all()])


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'college', 'mode']
    list_filter = ['name', 'college', 'mode']
    search_fields = ['name', 'college__name', 'mode']


admin.site.register(EducationDetails, EducationDetailsAdmin)

admin.site.register(Course, CourseAdmin)
admin.site.register(College, CollegeAdmin)
admin.site.register(Review)

# admin.site.register(Stream)
# admin.site.register(Facility)

admin.site.register(Inquiry)
admin.site.register(Testimonial)
admin.site.register(ExamDetail, ExamDetailAdmin)
