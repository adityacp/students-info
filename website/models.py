import pandas as pd

from django.db import models
from django.contrib.auth.models import User


def get_data(data_file, sheet_name=None):
    if "xls" in data_file._name or "xlsx" in data_file._name:
        df = pd.read_excel(data_file, sheet_name=sheet_name)
    elif "csv" in data_file._name:
        df = pd.read_csv(data_file)
    return df


class StudentManager(models.Manager):

    def add_students_to_db(self, data_file):
        status = False
        df = get_data(data_file, "Students")
        df.fillna("", inplace=True)
        user_data = df[
            ['ID','first_name', 'last_name', 'email', 'gender', 'school']
        ]
        book_data = df[['email', 'books']]
        book_data.rename(columns={"books": "book"}, inplace=True)
        book_data = book_data.to_dict("records")
        user_entries = user_data.to_dict("records")
        try:
            users = [
                User(
                    first_name=user.get("first_name"),
                    last_name=user.get("last_name"),
                    email=user.get("email"),
                    username=user.get("email")
                )
                for user in user_entries
            ]
            user_objects = User.objects.bulk_create(users)
            _user = [
                {"id": obj.id, "email": obj.email} for obj in user_objects
            ]
            user_df = pd.DataFrame(_user)
            students_data = pd.merge(user_data, user_df,
                        on='email', how='outer')
            students_data = students_data[['ID', 'id', 'school', 'gender']]
            students_data.rename(columns={'id': 'user_id'}, inplace=True)
            students_data = students_data.to_dict("records")
            students = [Student(**student) for student in students_data]
            books_data = [BookData(pages_read=10, **book) for book in book_data]
            Student.objects.bulk_create(students)
            BookData.objects.bulk_create(books_data)
            status = True
        except Exception as e:
            print(e)
            pass
        return status


class Student(models.Model):
    gender_choices = (("Male", "Male"), ("Female", "Female"), ('', ''))
    ID = models.PositiveBigIntegerField(default=0, unique=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student"
    )
    gender = models.CharField(
        max_length=10, choices=gender_choices, null=True, blank=True
    )
    school = models.CharField(max_length=255)
    objects = StudentManager()

    def __str__(self):
        return self.user.get_full_name()


class SchoolManager(models.Manager):

    def add_schools_to_db(self, data_file):
        status = False
        df = get_data(data_file, "Schools")
        df.fillna("", inplace=True)
        df.rename(columns={'school': 'name',
                  'address2': 'address',
                  'REGIONID': 'region_id'}, inplace=True)
        data = df.to_dict("records")
        schools = [School(**school) for school in data]
        try:
            School.objects.bulk_create(schools)
            status = True
        except Exception:
            pass
        return status


class School(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    principal = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    address = models.TextField()
    region_id = models.PositiveIntegerField(default=0)
    objects = SchoolManager()

    def __str__(self):
        return self.name


class BooksManager(models.Manager):

    def add_books_to_db(self, data_file):
        status = False
        df = get_data(data_file, "Books")
        df['Date of Publication'] = pd.to_datetime(
            df['Date of Publication']
        ).dt.date
        df.fillna("", inplace=True)
        df.rename(columns={'Title': 'title',
                  'Author Name': 'author',
                  'Date of Publication': 'date_of_publication',
                  'Number of Pages': 'no_of_pages'}, inplace=True)
        data = df.to_dict("records")
        books = [
            Book(
                date_of_publication=book.pop("date_of_publication") or None,
                **book
            )
            for book in data
        ]
        try:
            Book.objects.bulk_create(books)
            status = True
        except Exception:
            pass
        return status


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100, null=True, blank=True)
    date_of_publication = models.DateField(null=True, blank=True)
    no_of_pages = models.PositiveIntegerField()

    objects = BooksManager()

    def __str__(self):
        return self.title


class BookData(models.Model):
    email = models.EmailField()
    book = models.CharField(max_length=255)
    pages_read = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.book} read by {self.email}"
