
from django.contrib import admin
from django.db.models import Avg
from .models import Student, Grade, Course

class GradeInline(admin.TabularInline):
    model = Grade
    extra = 1
    fields = ('course', 'grade', 'date')
    ordering = ('-date',)
    autocomplete_fields = ('course',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'sex', 'active', 'short_name', 'avg_grade', 'courses_list')
    list_display_links = ('surname', 'name')
    search_fields = ('name', 'surname')
    list_filter = ('sex', 'active', 'course')
    filter_horizontal = ('course',)
    inlines = [GradeInline]
    list_per_page = 25
    ordering = ('surname', 'name')

    

    def short_name(self, obj):
        return f"{obj.surname} {obj.name[0]}."
    short_name.short_description = "Короткое имя"

    def avg_grade(self, obj):
        res = obj.grades.aggregate(avg=Avg('grade'))
        return round(res['avg'], 2) if res['avg'] is not None else '—'
    avg_grade.short_description = "Средний балл"

    def courses_list(self, obj):
        return ", ".join(f"{c.get_name_display()}-{c.course_num}" for c in obj.course.all())
    courses_list.short_description = "Курсы"

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    def course_name(self, obj):
        return obj.get_name_display()
    course_name.short_description = "Курс"

    list_display = ('course_name', 'course_num', 'start_date', 'end_date')
    list_filter = ('name', 'course_num', 'start_date', 'end_date')
    search_fields = ('description',)
    ordering = ('name', 'course_num')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('person', 'course', 'grade', 'date', 'date_add', 'date_update')
    list_filter = ('course', 'grade', 'date')
    search_fields = ('person__surname', 'person__name')
    autocomplete_fields = ('person', 'course')
    date_hierarchy = 'date'
    ordering = ('-date',)