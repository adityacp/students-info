from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse

from website.forms import SearchForm, StudentForm
from website.models import Student, BookData


def index(request):
    form = SearchForm()
    student_form = StudentForm()
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        student_name = request.POST.get("student_name")

        if student_id is None and student_name is None:
            return render(request, "website/index.html", {"form": form})

        if student_id:
            student = Student.objects.select_related("user").get(ID=student_id)
        else:
            student = Student.objects.select_related("user").get(
                Q(user__first_name__contains=student_name) | 
                Q(user__last_name__contains=student_name)
            )
        books = BookData.objects.filter(
            email=student.user.email
        ).values("book", "pages_read")
        context = {
            "name": student.user.get_full_name(),
            "email": student.user.email,
            "gender": student.gender,
            "school": student.school,
            "books": books
        }
        return render(
            request, "website/student_data.html", {"data": context.items()}
        )
    context = {"form": form, "add_form": student_form}
    return render(request, "website/index.html", context)


def student_data(request, student_id):
    student = Student.objects.select_related("user").get(ID=student_id)
    books = BookData.objects.filter(
        email=student.user.email
    ).values("book", "pages_read")
    context = {
        "name": student.user.get_full_name(),
        "email": student.user.email,
        "gender": student.gender,
        "school": student.school,
        "books": books
    }
    return render(
        request, "website/student_data.html", {"data": context.items()}
    )


def add_student(request):
    form = SearchForm()
    student_form = StudentForm()
    if request.method == "GET":
        return redirect(reverse("website:index"))
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        school = request.POST.get("schools")
        gender = request.POST.get("gender")
        books = request.POST.getlist("books")
        Id = request.POST.get("ID")
        try:
            user = User.objects.create(
                first_name=first_name, last_name=last_name,
                email=email, username=email
            )
            student = Student.objects.create(
                school=school, user_id=user.id,
                gender=gender, ID=Id
            )
            if books:
                book_data = [
                    BookData(email=user.email, book=book, pages_read=10)
                    for book in books
                ]
                book_objs = BookData.objects.bulk_create(book_data)
                books = [
                    {"book": book.book, "pages_read": book.pages_read}
                    for book in book_objs
                ]
            context = {
                "data": {
                    "name": student.user.get_full_name(),
                    "email": student.user.email,
                    "gender": student.gender,
                    "school": student.school,
                    "books": books
                }
            }
            template = "website/student_data.html"
        except Exception as e:
            context = {"form": form, "add_form": student_form, "error": e}
            template = "website/index.html"
    return render(request, template, context)

