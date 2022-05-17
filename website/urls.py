from django.urls import path
from website import views


urlpatterns = [
    path(r'', views.index, name="index"),
    path(r'student/info/<int:student_id>',
        views.student_data, name="student_data"),
    path(r'add/student/',
         views.add_student, name="add_student"),
]
