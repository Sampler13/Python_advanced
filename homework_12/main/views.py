from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from .models import Student, Course, Grade

def home(request):
    return render(request, 'home.html')

class StudentListView(ListView):
    model = Student
    template_name = 'students/students_list.html'
    context_object_name = 'students'
    paginate_by = 20
    queryset = (
        Student.objects.prefetch_related('course')
        .order_by('surname', 'name')
    )

class StudentDetailView(DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

    def get_queryset(self):
        return Student.objects.prefetch_related(
            'course',
            Prefetch('grades', queryset=Grade.objects.select_related('course').order_by('-date', '-id'))
        )

class CourseListView(ListView):
    model = Course
    template_name = 'courses/courses_list.html'
    context_object_name = 'courses'
    ordering = ('name', 'course_num')

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_queryset(self):
        return Course.objects.prefetch_related(
            Prefetch('student_set', queryset=Student.objects.order_by('surname', 'name'))
        )

def journal(request):
    students = (
        Student.objects.prefetch_related(
            Prefetch('grades', queryset=Grade.objects.select_related('course').order_by('date', 'id'))
        )
        .order_by('surname', 'name')
    )
    return render(request, 'journal.html', {'students': students})