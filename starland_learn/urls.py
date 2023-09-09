"""
URL configuration for starland_learn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from users.views import login, register, logout, profile, delete_account
from courses.views import (
    index,
    home,
    course_page,
    comment_controller,
    create_course,
    update_course,
    delete_course,
    search_courses,
)
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("logout/", logout, name="logout"),
    path("profile/", profile, name="profile"),
    path("home/", home, name="home"),
    path("delete_account/", delete_account, name="delete_account"),
    path("course/<int:course_id>/", course_page, name="course_page"),
    path(
        "course/<int:course_id>/comment", comment_controller, name="comment_controller"
    ),
    path("create_course/", create_course, name="create_course"),
    path("update_course/<int:course_id>/", update_course, name="update_course"),
    path("delete_course/<int:course_id>/", delete_course, name="delete_course"),
    path("search_courses/", search_courses, name="search_courses"),
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
