from django.contrib import admin
from django.contrib import messages
from django.urls import path
from django.http import HttpResponseRedirect

from website.models import Student, Book, School, BookData


class StudentAdmin(admin.ModelAdmin):
    change_list_template = "website/upload_students.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('add_students/', self.add_students),
        ]
        return my_urls + urls

    def add_students(self, request):
        if request.method == "POST" and "upload_students" in request.POST:
            file = request.FILES.get("student_file")
            status = Student.objects.add_students_to_db(file)
            if status:
                msg = "Students uploaded successfully"
                messages.add_message(request, messages.SUCCESS, msg)
            else:
                msg = "Failed to upload students data"
                messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect("../")


class SchoolAdmin(admin.ModelAdmin):
    change_list_template = "website/upload_schools.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('add_schools/', self.add_schools),
        ]
        return my_urls + urls

    def add_schools(self, request):
        if request.method == "POST" and "upload_schools" in request.POST:
            file = request.FILES.get("school_file")
            status = School.objects.add_schools_to_db(file)
            if status:
                msg = "Schools uploaded successfully"
                messages.add_message(request, messages.SUCCESS, msg)
            else:
                msg = "Failed to upload schools data"
                messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect("../")


class BookAdmin(admin.ModelAdmin):
    change_list_template = "website/upload_books.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('add_books/', self.add_books),
        ]
        return my_urls + urls

    def add_books(self, request):
        if request.method == "POST" and "upload_books" in request.POST:
            file = request.FILES.get("book_file")
            status = Book.objects.add_books_to_db(file)
            if status:
                msg = "Books uploaded successfully"
                messages.add_message(request, messages.SUCCESS, msg)
            else:
                msg = "Failed to upload books data"
                messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect("../")


admin.site.register(Student, StudentAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(BookData)
