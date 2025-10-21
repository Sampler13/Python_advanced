# seed_main.py
import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from main.models import Student, Course, Grade

def main():
    fake = Faker('ru_RU')

    courses = []
    for code, label in Course.langs:
        for i in range(1, 4):
            start_date = fake.date_between(start_date='-180d', end_date='-30d')
            end_date = fake.date_between(start_date='-29d', end_date='+60d')
            course, _ = Course.objects.get_or_create(
                name=code,
                course_num=i,
                defaults={
                    'start_date': start_date,
                    'end_date': end_date,
                    'description': f'{label} — поток {i}',
                }
            )
            courses.append(course)

    students = []
    for _ in range(50):
        first = fake.first_name()
        last = fake.last_name()
        student, _ = Student.objects.get_or_create(
            name=first,
            surname=last,
            defaults={
                'age': random.randint(18, 60),
                'sex': random.choice(['m', 'f', 'd']),
                'active': random.choice([True, False]),
            }
        )
        student.course.set(random.sample(courses, random.randint(1, min(4, len(courses)))))
        students.append(student)

    grades = []
    for st in students:
        st_courses = list(st.course.all())
        for _ in range(10):
            course = random.choice(st_courses)
            grade_val = random.randint(50, 100)
            date = fake.date_between(start_date='-90d', end_date='today')
            grades.append(Grade(person=st, course=course, grade=grade_val, date=date))

    if grades:
        Grade.objects.bulk_create(grades, batch_size=1000)

    print('Seed complete:',
          'courses =', Course.objects.count(),
          'students =', Student.objects.count(),
          'grades =', Grade.objects.count())

if __name__ == '__main__':
    main()