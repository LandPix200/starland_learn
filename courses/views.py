from django.http import HttpRequest
from django.shortcuts import render, redirect
from .models import Course, CourseComment
from django.shortcuts import render, redirect
from .forms import CourseForm


def index(request: HttpRequest):
    return redirect("home")


def home(request):
    courses = Course.objects.all()

    context = {"courses": courses}

    return render(request, "courses/home.html", context=context)


def course_page(request, course_id):
    course = Course.objects.get(pk=course_id)
    comments = CourseComment.objects.filter(course=course)

    return render(
        request,
        "courses/course_page.html",
        context={"course": course, "comments": comments},
    )


def comment_controller(request, course_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            comment = request.POST["comment"]
            user = request.user
            course = Course.objects.get(pk=course_id)
            CourseComment.objects.create(course=course, comment=comment, user=user)
        else:
            return redirect("login")

    return redirect("course_page", course_id=course_id)


def create_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.uploaded_by = request.user
            course.save()
            return redirect("course_page", course_id=course.pk)
    else:
        form = CourseForm()

    return render(request, "courses/create_course.html", {"form": form})


def update_course(request, course_id):
    course = Course.objects.get(pk=course_id)
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            course.uploaded_by = request.user
            course.save()
            return redirect("course_page", course_id=course.pk)
    else:
        form = CourseForm(instance=course)

    return render(
        request, "courses/update_course.html", {"form": form, "course": course}
    )


def delete_course(request, course_id):
    course = Course.objects.get(pk=course_id)
    course.delete()
    return redirect("home")


def search_courses(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        courses = Course.objects.filter(title__icontains=searched).order_by(
            "-created_at"
        )

        return render(
            request,
            "courses/search_courses.html",
            {
                "searched": searched,
                "courses": courses,
            },
        )

    return render(request, "courses/search_courses.html")
