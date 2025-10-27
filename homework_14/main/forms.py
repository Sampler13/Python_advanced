from django import forms
from .models import Student, Course

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'surname', 'age', 'sex', 'active', 'course']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 18, 'max': 100}),
            'sex': forms.Select(attrs={'class': 'form-select'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'course': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 6}),
        }
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'age': 'Возраст',
            'sex': 'Пол',
            'active': 'Активный',
            'course': 'Посещаемые курсы',
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'course_num', 'start_date', 'end_date', 'description']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-select'}),
            'course_num': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }