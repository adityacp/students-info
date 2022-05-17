from django import forms

from website.models import School, Book


class SearchForm(forms.Form):
    student_id = forms.CharField(
        label='Search by Id',
        widget=forms.TextInput(
            attrs={'placeholder': 'Search by student id'}),
        required=False
    )
    student_name = forms.CharField(
        label='Search by Name',
        widget=forms.TextInput(
            attrs={'placeholder': 'Search by student name'}),
        required=False
    )


class StudentForm(forms.Form):
    gender_choices = (("Male", "Male"), ("Female", "Female"), ('', ''))
    school_choices = (
        (name, name) for name in School.objects.values_list("name", flat=True)
    )
    book_choices = (
        (title, title) for title in Book.objects.values_list("title", flat=True)
    )
    ID = forms.IntegerField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=gender_choices)
    schools = forms.ChoiceField(choices=school_choices)
    books = forms.MultipleChoiceField(choices=book_choices)
