from django.db import models

from users.models import User
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _


def validate_video_file_extension(value):
    allowed_extensions = ['.mp4', '.webm']
    if not value.name.lower().endswith(tuple(allowed_extensions)):
        raise ValidationError(
            _('Seuls les fichiers vidéo MP4 et WebM sont autorisés.'))


class CourseManager(models.Manager):
    def create_course(self, title, description, file, uploaded_by):
        course = Course(
            title=title,
            description=description,
            file=file,
            uploaded_by=uploaded_by
        )
        course.save()
        return course

    def update_course(self, course_id, title=None, description=None, file=None):
        course: Course = self.get(pk=course_id)
        if title:
            course.title = title
        if description:
            course.description = description
        if file:
            course.file = file
        course.save()
        return course

    def delete_course(self, course_id):
        course: Course = self.get(pk=course_id)
        course.delete()

    def get_course(self, course_id):
        return self.get(pk=course_id)


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='courses_videos/',
                            validators=[validate_video_file_extension])
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ratings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title.__str__()

    objects = CourseManager()


class CourseComment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.email}"
