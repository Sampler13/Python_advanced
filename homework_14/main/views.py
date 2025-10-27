from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Prefetch
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Student, Course, Grade
from .forms import StudentForm, CourseForm


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

class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    permission_required = 'main.add_student'
    raise_exception = True
    def get_success_url(self):
        messages.success(self.request, 'Студент успешно создан.')
        return reverse('main:student_detail', args=[self.object.pk])


class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    permission_required = 'main.change_student'
    raise_exception = True
    def get_success_url(self):
        messages.success(self.request, 'Данные студента обновлены.')
        return reverse('main:student_detail', args=[self.object.pk])

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

class CourseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    permission_required = 'main.add_course'
    raise_exception = True
    def get_success_url(self):
        messages.success(self.request, 'Курс успешно добавлен.')
        return reverse('main:courses_list')

class CourseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    permission_required = 'main.delete_course'
    raise_exception = True
    def get_success_url(self):
        messages.success(self.request, 'Курс успешно удалён.')
        return reverse_lazy('main:courses_list')

class CourseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    permission_required = 'main.change_course'
    raise_exception = True
    def get_success_url(self):
        messages.success(self.request, 'Курс успешно обновлен.')
        return reverse('main:courses_list')


def journal(request):
    students = (
        Student.objects.prefetch_related(
            Prefetch('grades', queryset=Grade.objects.select_related('course').order_by('date', 'id'))
        )
        .order_by('surname', 'name')
    )
    return render(request, 'journal.html', {'students': students})