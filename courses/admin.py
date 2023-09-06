from django.contrib import admin

from .models import Course, CourseComment


admin.site.register(Course)
admin.site.register(CourseComment)
