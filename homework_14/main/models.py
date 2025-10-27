from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Student(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Имя',
        null=False,
        blank=False
    )

    surname = models.CharField(
        max_length=30,
        verbose_name='Фамилия'
    )

    age = models.SmallIntegerField(
        null=False,
        blank=False,
        verbose_name='Возраст',
        validators=[MinValueValidator(18), MaxValueValidator(100)]
    )

    sex = models.CharField(
        max_length=20,
        choices=[('m', 'мужчина'), ('f', 'женщина'), ('d', 'программист')],
        verbose_name='Пол'
    )

    active = models.BooleanField(
        verbose_name='Активный'
    )

    course = models.ManyToManyField(
                to='Course', 
                blank=True, 
                verbose_name="Посещаемые курсы")
    

    def __str__(self):
        return f"{self.id} {self.name} {self.surname} {self.age}"
    
        
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты" 
        indexes = [models.Index(fields=['surname'])]
        unique_together = [['name', 'surname']]
        ordering = ["surname"]

class Course(models.Model):
    langs = [
        ('py','Python'),
        ('js','JavaScript'),
        ('c','C++'),
        ('an','Android'),
    ]
    
    name = models.CharField(choices=langs, max_length=20, verbose_name="Курс")
    course_num = models.SmallIntegerField(
                    default=1, 
                    verbose_name="Номер курса", 
                    validators=[MinValueValidator(1), MaxValueValidator(100)]) 
    start_date = models.DateField(verbose_name = 'Начало курса', null=True)
    end_date = models.DateField(verbose_name = 'Окончание курса', null=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    
    def __str__(self):
        return f"{self.get_name_display()} - {self.course_num}"
    
    
    class Meta:
        unique_together = [['name', 'course_num']]
        verbose_name = "Курс"
        verbose_name_plural = "Курсы" 
        ordering = ['name', 'course_num']
        
    
        
class Grade(models.Model):
    person = models.ForeignKey(
            Student, 
            on_delete=models.CASCADE,
            related_name="grades",
            verbose_name = 'Чья оценка')
    
    grade = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name = 'Оценка'
    )
    
    course = models.ForeignKey(
            Course, 
            null=True,
            on_delete=models.CASCADE,
            verbose_name = 'Курс')
    
    date = models.DateField(verbose_name = 'Дата оценки', null=True)
    
    
    date_add = models.DateField(
            auto_now_add=True, 
            null=True,
            verbose_name = 'Дата добавления')
    
    date_update = models.DateField(
            auto_now=True,
            null=True,
            verbose_name = 'Дата изменения')

    

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"             
        
        

